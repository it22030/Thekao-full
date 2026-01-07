from django.urls import path
from django.contrib.auth import views as auth_views # Import built-in auth views
from . import views

urlpatterns = [
    # General Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Rider Specific
    # Make sure RiderRegisterView is actually a View class in views.py
    path('rider/register/', views.rider_register_view, name='rider_register'),
    path('rider/login/', views.RiderLoginView.as_view(), name='rider_login'),
]