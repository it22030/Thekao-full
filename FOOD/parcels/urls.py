from django.urls import path
from . import views

urlpatterns = [
    path('', views.parcel_home, name='parcel_home'),
    path('create/', views.create_parcel, name='create_parcel'),
    path('<int:parcel_id>/', views.parcel_detail, name='parcel_detail'),

    path('accept/<int:parcel_id>/', views.accept_parcel, name='accept_parcel'),
    path('pickup/<int:parcel_id>/', views.pickup_parcel, name='pickup_parcel'),
    path('deliver/<int:parcel_id>/', views.deliver_parcel, name='deliver_parcel'),
]
