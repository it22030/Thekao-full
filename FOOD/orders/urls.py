from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_order, name='create_order'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('create/cart/', views.create_order_from_cart, name='create_order_from_cart'),
]
