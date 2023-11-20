from django.db import models as m

class User(m.Model):
    given_name = m.CharField(max_length=30)
    family_name = m.CharField(max_length=30)
    username = m.CharField(max_length=30)
    can_buy = m.BooleanField()
    can_sell = m.BooleanField()
    # password_hash = 

# Gonna leave it at this
# Create your models here.
