from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import *
from django.contrib.auth.models import User
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

	user.is_staff = request.POST.get('privilieges')['IS_STAFF']
	user.is_superuser = request.POST.get('privilieges') [ 'IS_SUPERUSER']

	user.save()

	profile = Profile()
	profile.user = user
	profile.given_name = request.POST.get('given_name')
	profile.family_name = request.POST.get('family_name') 
	profile.can_buy = request.POST.get('user_role')['buyer']
	profile.can_sell = request.POST.get('user_role')['seller']
	profile.diet_reqs.set(CONTAINS[id] for id in request.POST.getlist('diets'))
	profile.rating = None
	profile.location = request.POST.get('location')
	profile.save()

	return HttpResponse("User Created")


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

def delete_listing(request):
	listing = Meal.objects.get(id=request.POST.get('meal_ID'))
	listing.delete()

	return HttpResponse("Listing deleted")

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