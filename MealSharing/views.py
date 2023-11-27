from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import auth
from . import dbops

# Contains.objects.bulk_create(
# 	CONTAINS := [
# 		Contains(id = 0, name="Vegan"),
# 		Contains(id=1, name="Dairy"),
# 		Contains(id=2, name="Eggs"),
# 		Contains(id=3, name="Gluten"),
# 		# ...
# 	])

# Rating.objects.bulk_create(
# 	RATINGS := [
# 	Rating(code="A+", name="Very Good"), 
# 	Rating(code="A", name="Good"),
# 	Rating(code="B", name="Okay"),
# 	Rating(code="C", name="Fair"), 
# 	Rating(code="D", name="Bad"),
# ])

@login_required
def create_user(request):
	if request.method == 'POST':
		result = dbops.create_user(request)
		return HttpResponse(result)
	else:
		return HttpResponse("POST request required.")
	
@login_required
def add_user(request):
	if request.user.is_staff: form = StaffMakeUserForm
	if request.user.is_superuser: form = SuperuserMakeUserForm
	else: form = CreateUserForm
	context = {'form': form}
	if request.method == "POST":
		dbops.create_user(request)
	return render(request, "make_user.html", context)

def register(request):
	return render(request, 'make_user.html', {'form' : CreateUserForm})

@login_required
def change_user(request):
	if(request.method == "POST"):
		dbops.update_profile(request)
	return render(request, "home.html")

# Update Profile
@login_required  
def update_profile(request):
	if request.method == 'POST':
		result = dbops.update_profile(request)
		return HttpResponse(result)
	else:
		return HttpResponse("POST request required.")

# Make Listing
@login_required
def make_listing(request):
	if request.method == 'POST':
		result = dbops.make_listing(request)  
		return HttpResponse(result)
	else:
		return HttpResponse("POST request required.")
		
# Delete Listing
@login_required  
def delete_listing(request):
	if request.method == 'POST':
		result = dbops.delete_listing(request)
		return HttpResponse(result)
	else:
		return HttpResponse("POST request required.")
			
# Buy Meal  
@login_required
def buy_meal(request):
	if request.method == 'POST':
		result = dbops.buy_meal(request)
		return HttpResponse(result)
	else:
		return HttpResponse("POST request required.")
		
# Cancel Order
@login_required         
def cancel_order(request):
	if request.method == 'POST':
		result = dbops.cancel_order(request)
		return HttpResponse(result)
	else:
		return HttpResponse("POST request required.")
	
def home(request):
	return render(request, 'home.html')

# profile view
@login_required
def profile(request):
	user = request.user
	profile = dbops.get_profile(request)
	return render(request, 'profile.html', profile)
	
# edit_profile view  
@login_required
def edit_profile(request):
	if request.method == 'POST':
		result = dbops.update_profile(request)
		return HttpResponseRedirect('/profile')
	else:
		profile = dbops.get_profile(requestusr := request.GET.get('requested_user') if requestusr else request.user)
		return render(request, 'edit_profile.html', {"profile": profile})
	
def listingmgmt(request):
	if request.method == 'POST':
		return render(request, 'home.html', status=300)
	else:
		meals = dbops.seemeals(request)
		return render(request, 'lstmgmt.html', {'form' : MealListingMaker})
		
# login view
def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username=username, password=password)
		if user is not None:
			auth.login(request, user)
			return HttpResponseRedirect('/')
		else:
			return render(request, 'login.html')
	else:
		return render(request, 'login.html')
	
		 
# logout view       
@login_required
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/')