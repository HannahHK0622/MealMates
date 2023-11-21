from django.urls import path, include
from MealSharing import views

urlpatterns = [
  path('admin/', views.home),
  path('mealMates/', include('MealSharing.urls'))
]