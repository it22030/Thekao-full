from django.urls import path
from . import views

urlpatterns = [
    path('', views.mall_home, name='mall_home'),
    path('shop/<int:shop_id>/', views.shop_detail, name='shop_detail'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    
    # Cart
    path('cart/', views.view_cart, name='mall_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_mall_cart'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_mall_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_mall_cart'),
    
    # Checkout & Orders
    path('checkout/', views.checkout, name='mall_checkout'),
    path('orders/', views.my_mall_orders, name='my_mall_orders'),
    path('order/<int:order_id>/', views.order_detail, name='mall_order_detail'),
]
