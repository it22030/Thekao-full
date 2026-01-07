import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Food_delivery.settings')
django.setup()

from restaurants.models import Restaurant
from menu.models import MenuItem
from mall.models import Shop, Product

def add_products():
    print("Adding Products to Food and Mall...")

    # ==========================
    # FOOD (Restaurants & Menu)
    # ==========================
    
    # 1. KFC
    kfc, _ = Restaurant.objects.get_or_create(
        name="KFC",
        defaults={
            "description": "It's Finger Lickin' Good",
            "address": "789 Fried Chicken Blvd",
            "image": "https://images.unsplash.com/photo-1513639776629-7b611d22f654?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80", # Generic chicken image
            "rating": 4.5
        }
    )
    
    MenuItem.objects.get_or_create(
        restaurant=kfc,
        name="Zinger Burger Meal",
        defaults={
            "description": "Spicy Zinger burger with regular fries and a drink.",
            "price": 450.00,
            "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
        }
    )

    MenuItem.objects.get_or_create(
        restaurant=kfc,
        name="Hot Wings (6pcs)",
        defaults={
            "description": "Spicy and crispy chicken wings.",
            "price": 299.00,
            "image": "https://images.unsplash.com/photo-1527477396000-e27163b481c2?ixlib=rb-1.2.1&auto=format&fit=crop&w=1353&q=80"
        }
    )

    # 2. Nando's
    nandos, _ = Restaurant.objects.get_or_create(
        name="Nando's",
        defaults={
            "description": "Legendary Peri-Peri Chicken",
            "address": "456 Peri Peri Lane",
            "image": "https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
            "rating": 4.7
        }
    )
    
    MenuItem.objects.get_or_create(
        restaurant=nandos,
        name="1/4 Chicken Meal",
        defaults={
            "description": "Quarter chicken marinated in Peri-Peri sauce with 2 sides.",
            "price": 650.00,
            "image": "https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
        }
    )

    # ==========================
    # MALL (Shops & Products)
    # ==========================
    
    # 1. Tech World (Electronics)
    tech_world, _ = Shop.objects.get_or_create(
        name="Tech World",
        defaults={
            "description": "Latest gadgets and electronics",
            "address": "Level 1, City Mall",
            "image": "https://images.unsplash.com/photo-1531297461136-82lw9z2157l8?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
        }
    )
    
    Product.objects.get_or_create(
        shop=tech_world,
        name="Wireless Noise Cancelling Headphones",
        defaults={
            "description": "Premium sound quality with active noise cancellation.",
            "price": 12000.00,
            "stock": 50,
            "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
        }
    )

    Product.objects.get_or_create(
        shop=tech_world,
        name="Smart Watch Series 5",
        defaults={
            "description": "Track your fitness and stay connected.",
            "price": 8500.00,
            "stock": 30,
            "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
        }
    )

    # 2. Fashion Avenue (Clothing)
    fashion_ave, _ = Shop.objects.get_or_create(
        name="Fashion Avenue",
        defaults={
            "description": "Trendy fashion for men and women",
            "address": "Level 2, City Mall",
            "image": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
        }
    )

    Product.objects.get_or_create(
        shop=fashion_ave,
        name="Denim Jacket",
        defaults={
            "description": "Classic blue denim jacket.",
            "price": 2500.00,
            "stock": 100,
            "image": "https://images.unsplash.com/photo-1523205771623-e0faa4d2813d?ixlib=rb-1.2.1&auto=format&fit=crop&w=1353&q=80"
        }
    )

    Product.objects.get_or_create(
        shop=fashion_ave,
        name="Casual Sneakers",
        defaults={
            "description": "Comfortable white sneakers for everyday wear.",
            "price": 3200.00,
            "stock": 75,
            "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
        }
    )

    print("Success! Added new products to Food and Mall.")

if __name__ == "__main__":
    add_products()
