from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

from .views import landing_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('orders/', include('orders.urls')),
    path('restaurants/', include('restaurants.urls')),
    path('menu/', include('menu.urls')),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('cart.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('rides/', include('rides.urls')),
    path('mall/', include('mall.urls')),
    path('parcels/', include('parcels.urls')),
    path('', landing_page, name='home'),
]
