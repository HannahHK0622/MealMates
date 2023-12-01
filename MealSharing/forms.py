from django import forms as f
from django.contrib.auth.models import User
from .models import *


class CreateUserForm(f.Form):
	
	username = f.CharField()
	email = f.EmailField()
	password = f.CharField(widget=f.PasswordInput)
	given_name = f.CharField()
	family_name = f.CharField()
	can_buy = f.BooleanField(required=False)
	can_sell = f.BooleanField(required=False)
	diets = f.MultipleChoiceField(
		label="dietary requirements",
		widget= f.SelectMultiple,
		choices = [(diet.id, diet.name) for diet in Contains.objects.all()],
		required=False 
	)
	location = f.CharField(required=False)

class StaffMakeUserForm(CreateUserForm):
	is_staff = f.BooleanField(required = False)
	  
class SuperuserMakeUserForm(StaffMakeUserForm):
	is_superuser = f.BooleanField(required=False)

class MealListingMaker(f.Form):
	food_class = f.MultipleChoiceField(
		label = "allergens & food classes",
		widget= f.SelectMultiple(attrs={'size':Contains.objects.count()}),
		choices = ((diet.id, diet.name) for diet in Contains.objects.all()),
		required=False 
	)
	price = f.FloatField()
	sell_by = f.DateField(widget=f.SelectDateWidget)
	number_listed = f.IntegerField()
	internal_id = f.CharField(max_length=40, required=False)

class MealListingEditor(MealListingMaker):
	delete = f.BooleanField(required=False)

	def populate(self, meal_data):
		meal = next(iter(meal_data.values()))
		self.initial = {k:v for k,v in meal.items() if k in self.fields}

class MakeOrder(f.Form):
	meal_id = f.IntegerField()
	date_bought = f.DateField()

