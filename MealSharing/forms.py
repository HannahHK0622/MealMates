from django import forms as f
from django.contrib.auth.models import User
from .models import *


class CreateUserForm(f.Form):
    username = f.CharField()
    email = f.EmailField()
    password = f.CharField(widget=f.PasswordInput)
    is_staff = f.BooleanField(required=False)
    is_superuser = f.BooleanField(required=False)
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