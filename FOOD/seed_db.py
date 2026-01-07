import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Food_delivery.settings')
django.setup()

from restaurants.models import Restaurant
from menu.models import MenuItem

def seed():
    # Existing Restaurants
    r1, _ = Restaurant.objects.get_or_create(
        name="Burger King",
        defaults={
            "description": "Home of the Whopper",
            "address": "123 Main St",
            "image": "https://images.unsplash.com/photo-1571091718767-18b5b1457add?ixlib=rb-1.2.1&auto=format&fit=crop&w=1352&q=80",
            "rating": 4.2
        }
    )

    MenuItem.objects.get_or_create(
        restaurant=r1,
        name="Whopper Meal",
        defaults={
            "description": "Flame-grilled beef patty, sesame bun, mayo, lettuce, tomato, pickles, ketchup, onions.",
            "price": 9.99,
            "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?ixlib=rb-1.2.1&auto=format&fit=crop&w=902&q=80"
        }
    )
    
    MenuItem.objects.get_or_create(
        restaurant=r1,
        name="Chicken Royale",
        defaults={
            "description": "Crispy chicken breast with lettuce and mayo.",
            "price": 7.49,
            "image": "https://images.unsplash.com/photo-1615557960916-5f4791effe9d?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80"
        }
    )

    r2, _ = Restaurant.objects.get_or_create(
        name="Pizza Hut",
        defaults={
            "description": "Pizza, Pasta, and Wings",
            "address": "456 Elm St",
            "image": "https://images.unsplash.com/photo-1590947132387-155cc02f3212?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
            "rating": 4.0
        }
    )

    MenuItem.objects.get_or_create(
        restaurant=r2,
        name="Pepperoni Feast",
        defaults={
            "description": "Double pepperoni and mozzarella.",
            "price": 14.99,
            "image": "https://images.unsplash.com/photo-1628840042765-356cda07504e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80"
        }
    )

    # New Restaurants
    r3, _ = Restaurant.objects.get_or_create(
        name="Sushi Zen",
        defaults={
            "description": "Authentic Japanese Sushi and Sashimi",
            "address": "789 Sakura Ln",
            "image": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
            "rating": 4.8
        }
    )

    MenuItem.objects.get_or_create(
        restaurant=r3,
        name="Dragon Roll",
        defaults={
            "description": "Shrimp tempura, eel, avocado, and cucumber.",
            "price": 16.99,
            "image": "https://images.unsplash.com/photo-1617196034738-26c5f7c977ce?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80"
        }
    )

    MenuItem.objects.get_or_create(
        restaurant=r3,
        name="Nigiri Platter",
        defaults={
            "description": "Assorted fresh fish over seasoned rice.",
            "price": 22.50,
            "image": "https://images.unsplash.com/photo-1583623025817-d180a2221d0a?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80"
        }
    )

    r4, _ = Restaurant.objects.get_or_create(
        name="Taco Bell",
        defaults={
            "description": "Live Mas with our Mexican-inspired favorites",
            "address": "321 Fiesta Ave",
            "image": "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
            "rating": 4.1
        }
    )

    MenuItem.objects.get_or_create(
        restaurant=r4,
        name="Crunchwrap Supreme",
        defaults={
            "description": "A flour tortilla layered with seasoned beef, nacho cheese sauce, and a crunchy tostada shell.",
            "price": 5.49,
            "image": "https://images.unsplash.com/photo-1599974590229-271ffdd326e4?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80"
        }
    )

    r5, _ = Restaurant.objects.get_or_create(
        name="The Pasta House",
        defaults={
            "description": "Traditional Italian Pasta and Wine",
            "address": "555 Roma Blvd",
            "image": "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
            "rating": 4.6
        }
    )

    MenuItem.objects.get_or_create(
        restaurant=r5,
        name="Fettuccine Alfredo",
        defaults={
            "description": "Rich and creamy alfredo sauce with fettuccine pasta.",
            "price": 13.99,
            "image": "https://images.unsplash.com/photo-1645112481338-35624ba74fd6?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80"
        }
    )

    r6, _ = Restaurant.objects.get_or_create(
        name="Green Garden",
        defaults={
            "description": "Fresh and healthy salads for every taste",
            "address": "111 Leafy Rd",
            "image": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
            "rating": 4.5
        }
    )

    MenuItem.objects.get_or_create(
        restaurant=r6,
        name="Quinoa Power Bowl",
        defaults={
            "description": "Quinoa, kale, roasted vegetables, and a lemon tahini dressing.",
            "price": 11.49,
            "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80"
        }
    )

    print("Database seeded successfully with more restaurants!")

if __name__ == '__main__':
    seed()
