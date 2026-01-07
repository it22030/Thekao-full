from django.urls import path
from . import views

app_name = 'rides'

urlpatterns = [


    path('', views.ride_home, name='ride_home'),
    path('create/', views.create_ride, name='create_ride'),
    path('<int:ride_id>/', views.ride_detail, name='ride_detail'),

    path('accept/<int:ride_id>/', views.accept_ride, name='accept_ride'),
    path('start/<int:ride_id>/', views.start_ride, name='start_ride'),
    path('complete/<int:ride_id>/', views.complete_ride, name='complete_ride'),
    path('api/updates/<int:ride_id>/', views.get_ride_updates, name='get_ride_updates'),
   path("shared/", views.shared_rides, name="shared_rides"),

]
