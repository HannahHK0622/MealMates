from django.urls import path, include
from django.contrib import admin
from MealSharing import views

urlpatterns = [
  path('admin/', admin.site.urls),
  path('', include('MealSharing.urls'))
]