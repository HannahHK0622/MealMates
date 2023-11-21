from django.db import models as m
from django.core.validators import int_list_validator as ilv

class Contains(m.Model):
    id = m.IntegerField(primary_key=True)
    name = m.CharField(max_length=16)

class Rating(m.Model):
    code = m.CharField(max_length=2, primary_key=True)
    name = m.CharField(max_length=8)

CONTAINS = [
    Contains(id=1, name="Dairy"),
    Contains(id=2, name="Eggs"),
    Contains(id=3, name="Gluten"),
    ...
]

RATINGS = [
   Rating(code="A+", name="Very Good"), 
   Rating(code="A", name="Good"),
   Rating(code="B", name="Okay"),
   Rating(code="C", name="Fair"), 
   Rating(code="D", name="Bad"),
]

class User(m.Model):
    given_name = m.CharField(max_length=30)
    family_name = m.CharField(max_length=30)
    username = m.CharField(max_length=30)
    can_buy = m.BooleanField()
    can_sell = m.BooleanField()
    diet_reqs = m.ManyToManyField(Contains)
    rating = m.ForeignKey(
        Rating, 
        on_delete=m.SET_NULL,
        null=True)
    location = m.CharField(max_length=100)

class Meal(m.Model):
    meal_id = m.IntegerField(primary_key=True)
    seller = m.ForeignKey(
        User,
        on_delete=m.CASCADE,
        related_name="Seller"
    )
    buyer = m.ForeignKey(
        User, 
        on_delete=m.CASCADE,
        null=True,
        related_name="Buyer"
    )
    food_class = m.ManyToManyField(Contains)
    price=m.FloatField()
    listed_date=m.DateField()
    sell_by=m.DateField()
    internal_id = m.CharField(max_length=40)
    order_id = m.CharField(max_length=20)
# Create your models here.
