from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('login/', views.login),
    path('logout/', views.logout),
	path('add-user/', views.add_user, name='add-user'), 
    path('change-user/<int:pk>/', views.change_user, name='change-user'),
]
