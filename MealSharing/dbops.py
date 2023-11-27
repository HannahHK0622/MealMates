from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

import datetime


# POST /users
def create_user(request):

	username = request.POST.get('username')  
	email = request.POST.get('email')
	password = request.POST.get('password')

	user = User()
	user.username = username
	user.email = email
	user.set_password(password)

	user.is_staff = bool(request.POST.get('is_staff'))
	user.is_superuser = bool(request.POST.get('is_superuser'))

	user.save()

	profile = Profile()
	profile.user = user
	profile.given_name = request.POST.get('given_name')
	profile.family_name = request.POST.get('family_name') 
	profile.can_buy = bool(request.POST.get('is_buyer'))
	profile.can_sell = bool(request.POST.get('is_seller'))
	profile.rating = None
	profile.location = request.POST.get('location')
	profile.save()
	profile.diet_reqs.set(CONTAINS[id] for id in request.POST.getlist('diets'))
	profile.save()

	return HttpResponse("User Created")

@login_required
def get_profile(request):
	user = request.GET.get('requested_user')
	try:
		profile = Profile.objects.get(user=user)
	except:
		return HttpResponse(f"request.GET.get('requested_user') does not exist.")
	if user != request.user:
		if request.user.is_staff or request.user.is_superuser:
			pass
		else: return HttpResponse(f"{request.user.username} is not authenticated to see {user.username}.")
	return({
		"id": user.id,
		"username": user.username,
		"email": user.email,
		"given_name": profile.given_name,
		"family_name": profile.family_name,
		"can_buy": profile.can_buy,
		"can_sell": profile.can_sell,
		"diet": profile.diet_reqs,
		"rating": profile.rating,
		"location": profile.location
	}) 

@login_required
def update_profile(request):
	userprofile = get_profile(request)
	if (userprofile[id] != request.user.id 
		and not(
		request.user.is_admin or
		request.user.is_superuser)):
		return HttpResponse(f"{request.user.id} is not authenticated to change the details of {userprofile[id]}.")
	username = request.POST.get('username')  
	email = request.POST.get('email')
	password = request.POST.get('password') if request.POST.get('password') else ""

	user = User.objects.get(id = userprofile.id)
	user.username = username
	user.email = email
	if(password):
		user.set_password(password)

	user.is_staff = request.POST.get('privilieges')['IS_STAFF']
	user.is_superuser = request.POST.get('privilieges') [ 'IS_SUPERUSER']

	user.save()

	profile = Profile.objects.get(user=user)
	profile.user = user
	profile.given_name = request.POST.get('given_name')
	profile.family_name = request.POST.get('family_name') 
	profile.can_buy = request.POST.get('user_role')['buyer']
	profile.can_sell = request.POST.get('user_role')['seller']
	profile.diet_reqs.set(CONTAINS[id] for id in request.POST.getlist('diets'))
	profile.rating = None
	profile.location = request.POST.get('location')
	profile.save()


@login_required
def make_listing(request):
	seller = request.POST.get('seller')
	price = request.POST.get('price')

	listing = Meal()
	listing.seller = seller
	listing.price = price
	listing.listed_date = datetime.date.today()
	listing.diet_class.set(CONTAINS[id] for id in request.POST.getlist('diets'))

	listing.save()

	return HttpResponse("Listing Created")

@login_required
def delete_listing(request):
	listing = Meal.objects.get(id=request.POST.get('meal_ID'))
	listing.delete()

	return HttpResponse("Listing deleted")

@login_required
def buy_meal(request):
	buyer = request.user
	if not buyer.can_buy:
		return HttpResponse(f"{request.user.username} does not have permission to buy.")
	order = Order()
	order.buyer = request.user
	order.date_bought = datetime.date.today()

def cancel_order(request):
	buyer = request.user
	order = request.order.id
	if(
		not buyer.can_buy
		or
		order.buyer is not request.user
	):
		return HttpResponse(f"{buyer.username} has no privilieges to cancel {order.id}")