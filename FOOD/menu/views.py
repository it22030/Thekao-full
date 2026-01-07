from django.shortcuts import render, get_object_or_404
from restaurants.models import Restaurant
from .models import MenuItem

def menu_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_items = restaurant.menu_items.filter(is_available=True)
    return render(request, 'menu/menu_detail.html', {'restaurant': restaurant, 'menu_items': menu_items})
