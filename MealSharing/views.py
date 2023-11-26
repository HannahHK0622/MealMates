from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from . import dbops

@login_required
def create_user(request):
	if request.method == 'POST':
		result = dbops.create_user(request)
		return HttpResponse(result)
	else:
		return HttpResponse("POST request required.")
@login_required
def add_user(request):
	if request.method == "POST":
		dbops.create_user(request)
	return render(request, "home.html  ")

@login_required
def change_user(request):
	if(request.method == "POST"):
		dbops.update_profile(request)
	return 

@login_required
def get_profile(request):
	if request.method == 'GET':
		result = dbops.get_profile(request)
		return HttpResponse(result)
	else: 
		return HttpResponse("GET request required.")

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
	return render(request, 'profile.html', {'profile': profile})
	
# edit_profile view  
@login_required
def edit_profile(request):
	if request.method == 'POST':
		result = dbops.update_profile(request)
		return HttpResponseRedirect('/profile')
	else:  
		return render(request, 'edit_profile.html')
		
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