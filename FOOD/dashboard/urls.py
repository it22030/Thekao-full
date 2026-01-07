from django.urls import path
from . import views

urlpatterns = [
    # Admin routes
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('users/', views.manage_users, name='manage_users'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('restaurants/', views.manage_restaurants, name='manage_restaurants'),
    path('restaurants/add/', views.add_restaurant, name='add_restaurant'),
    path('restaurants/delete/<int:restaurant_id>/', views.delete_restaurant, name='delete_restaurant'),
    path('settings/', views.manage_settings, name='manage_settings'),
    path('orders/', views.manage_orders, name='manage_orders'),
    path('orders/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('orders/assign-rider/<int:order_id>/', views.assign_rider, name='assign_rider'),
    path('riders/', views.manage_riders, name='manage_riders'),
    path('rides/', views.manage_rides, name='manage_rides'),
    path('rides/assign-rider/<int:ride_id>/', views.assign_ride, name='assign_ride'),
    
    # Rider Management
    path('rider/update-services/<int:rider_id>/', views.update_rider_services, name='update_rider_services'),
    
    # Mall & Parcels
    path('mall/shops/', views.manage_shops, name='manage_shops'),
    path('mall/orders/', views.manage_mall_orders, name='manage_mall_orders'),
    path('parcels/', views.manage_parcels, name='manage_parcels'),
    path('parcels/assign-rider/<int:parcel_id>/', views.assign_parcel_rider, name='assign_parcel_rider'),

    # Rider routes
    path('rider/', views.rider_dashboard, name='rider_dashboard'),
    path('rider/available-orders/', views.available_orders, name='available_orders'),
    path('rider/accept-order/<int:order_id>/', views.accept_order, name='accept_order'),
    path('rider/update-order-status/<int:order_id>/', views.update_order_status, name='update_order_status'),

    # Mall Rider routes
    path('rider/mall-available/', views.available_mall_orders, name='available_mall_orders'),
    path('rider/mall-accept/<int:order_id>/', views.accept_mall_order, name='accept_mall_order'),
    path('rider/mall-update-status/<int:order_id>/', views.update_mall_order_status, name='update_mall_order_status'),
]
