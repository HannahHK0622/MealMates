from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

import datetime


# POST /users
def create_user(request):
	form = SuperuserMakeUserForm()

	username = request.POST.get('username')  
	email = request.POST.get('email')
	password = request.POST.get('password')

	user = User()
	user.username = username
	user.email = email
	user.set_password(password)

	user.is_staff = request.POST.get('is_staff') == 'on'
	user.is_superuser = request.POST.get('is_superuser') == 'on'

	user.save()

	profile = Profile()
	profile.user = user
	profile.given_name = request.POST.get('given_name')
	profile.family_name = request.POST.get('family_name') 
	profile.can_buy = request.POST.get('can_buy') == 'on'
	profile.can_sell = request.POST.get('can_sell') == 'on'
	profile.rating = None
	profile.location = request.POST.get('location')
	profile.save()
	profile.diet_reqs.set(CONTAINS[id] for id in request.POST.getlist('diets'))
	profile.save()

	return HttpResponse("User Created")

@login_required
def get_profile(request):
	user = request.GET.get('requested_user')
	user = request.user 
	try:
		profile = Profile.objects.get(user=user)
	except:
		pass
	if user != request.user:
		if request.user.is_staff or request.user.is_superuser:
			pass
		
	return(
	# 	{"information": "value"}
	# )
		{"information" :{
		"id": user.id,
		"username": user.username,
		"email": user.email,
		"given_name": profile.given_name,
		"family_name": profile.family_name,
		"can_buy": profile.can_buy,
		"can_sell": profile.can_sell,
		"diet": profile.diet_reqs.all(),
		"rating": profile.rating,
		"location": profile.location
	}}) 

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

	user.is_staff = bool(request.POST.get('is_staff'))
	user.is_superuser = bool(request.POST.get('is_superuser'))

	user.save()

	profile = Profile.objects.get(user=user)
	profile.user = user
	profile.given_name = request.POST.get('given_name')
	profile.family_name = request.POST.get('family_name') 
	profile.can_buy = bool(request.POST.get('is_buyer'))
	profile.can_sell = bool(request.POST.get('is_seller'))
	profile.diet_reqs.set(CONTAINS[id] for id in request.POST.getlist('diets'))
	profile.rating = None
	profile.location = request.POST.get('location')
	profile.save()


@login_required
def make_listing(request):
	print("The request is", request.POST)

	update_meal(request)

	return HttpResponse("Listing Created")

def update_meal(request):
	seller = request.user
	price = request.POST.get('price')
	listing = Meal() if not (idx := request.POST.get('meal_id')) else Meal.objects.get(meal_id = idx)
	listing.seller = seller
	listing.price = price
	listing.listed_date = datetime.date.today()
	listing.sell_by = datetime.datetime(*(map(int,
											map(request.POST.get,
												("sell_by_year", "sell_by_month", "sell_by_day")))))
	listing.save()

	print(listing.meal_id, "listing id is")

	try:
		id = [*map(
				int,
				request.POST.getlist('food_class')
			)]
		print(id)
		listing.food_class.set(id)
		
	except:
		listing.food_class.clear()

	finally:	
		listing.save()

@login_required
def delete_listing(request):
	listing = Meal.objects.get(id=request.POST.get('meal_ID'))
	listing.delete()

	return HttpResponse("Listing deleted")

@login_required
def buy_meal(request, pk):
	meal = Meal.objects.get(meal_id=pk)
	buyer = request.user
	order = Order()
	order.buyer = buyer
	order.date_bought = datetime.date.today()
	order.meal = meal
	order.save(force_insert=True)
	meal.shown = False
	meal.number_listed -= 1
	meal.save()

def cancel_order(request, pk):
	buyer = request.user
	order = request.POST.get(id = pk)
	meal = request.POST.get(order.meal_id)


	
def get_meal(request, idx=None):
	listings = Meal.objects.all() if not idx else [Meal.objects.get(meal_id=idx)]
	meal_details = {}
	iter = 0
	for listing in listings:
		meal_details[f'meal{iter}']= {
				"id": listing.meal_id,
				"seller": listing.seller.id,
				"food_class": listing.food_class.all(),
				"price": listing.price,
				"listed_date": listing.listed_date,
				"sell_by": listing.sell_by,
				"showable": listing.shown,
				"remaining": listing.number_listed
			}
		
		iter += 1
	return(
		meal_details
	)

def get_orders(request):
	"""
	orders should be like:
	f"order{order.id}": {
				"id": meal.meal_id,
				"seller": meal.seller.id,
				"food_class": meal.food_class.all(),
				"price": meal.price,
				"date_bought": order.date_bought
				}
	}
	"""

	orders = Order.objects.filter(buyer=request.user)
	order_details = {}
	iter = 0
	for order in orders:
		meal = Meal.objects.get(meal_id = order.meal.meal_id)
		order_details[f"order{iter}"] = {
				"id": order.id,
				"meal_id": meal.meal_id,
				"seller": meal.seller.id,
				"food_class": meal.food_class.all(),
				"price": meal.price,
				"date_bought": order.date_bought
 		}
		iter += 1

	return order_details