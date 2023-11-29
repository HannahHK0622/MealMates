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
	path('make-user/', views.add_user, name='add-user'),
	path('register/', views.register, name='register'),
    path('browse/', views.listingmgmt, name='browse-meals'),
	path('list/', views.make_listing, name='make-listing'),
    path('edit_meal/<int:id>', views.edit_meal, name='edit_meal'),
	path('buy/<int:pk>', views.purchase, name='purchase'),
	path('delete_order/<int:pk>', views.delete_order, name='delete-order'),
	path('edit_purchase', views.edit_purchase, name="edit_purchase")
]
