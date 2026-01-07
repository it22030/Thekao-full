from django.core.management.base import BaseCommand
from restaurants.models import Restaurant
from menu.models import MenuItem


class Command(BaseCommand):
    help = 'Add more diverse menu items to restaurants'

    def handle(self, *args, **kwargs):
        restaurants = Restaurant.objects.all()
        
        if not restaurants.exists():
            self.stdout.write(self.style.ERROR('No restaurants found. Please create restaurants first.'))
            return

        # Menu items data with BDT prices
        menu_data = {
            'Pizza Items': [
                {'name': 'Margherita Pizza', 'description': 'Classic tomato sauce, fresh mozzarella, basil', 'price': 650, 'image': 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400'},
                {'name': 'Pepperoni Pizza', 'description': 'Spicy pepperoni, mozzarella, tomato sauce', 'price': 750, 'image': 'https://images.unsplash.com/photo-1628840042765-356cda07504e?w=400'},
                {'name': 'BBQ Chicken Pizza', 'description': 'Grilled chicken, BBQ sauce, red onions, cilantro', 'price': 850, 'image': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400'},
                {'name': 'Vegetarian Supreme', 'description': 'Bell peppers, mushrooms, olives, onions, tomatoes', 'price': 700, 'image': 'https://images.unsplash.com/photo-1511689660979-10d2b1aada49?w=400'},
            ],
            'Burgers': [
                {'name': 'Classic Beef Burger', 'description': 'Juicy beef patty, lettuce, tomato, pickles, special sauce', 'price': 450, 'image': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400'},
                {'name': 'Cheese Burger Deluxe', 'description': 'Double beef patty, cheddar cheese, bacon, onion rings', 'price': 550, 'image': 'https://images.unsplash.com/photo-1550547660-d9450f859349?w=400'},
                {'name': 'Chicken Burger', 'description': 'Crispy fried chicken, coleslaw, mayo, lettuce', 'price': 400, 'image': 'https://images.unsplash.com/photo-1606755962773-d324e0a13086?w=400'},
                {'name': 'Veggie Burger', 'description': 'Plant-based patty, avocado, sprouts, chipotle mayo', 'price': 420, 'image': 'https://images.unsplash.com/photo-1520072959219-c595dc870360?w=400'},
            ],
            'Sushi & Japanese': [
                {'name': 'California Roll', 'description': 'Crab, avocado, cucumber, sesame seeds', 'price': 550, 'image': 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400'},
                {'name': 'Spicy Tuna Roll', 'description': 'Fresh tuna, spicy mayo, cucumber, scallions', 'price': 650, 'image': 'https://images.unsplash.com/photo-1553621042-f6e147245754?w=400'},
                {'name': 'Dragon Roll', 'description': 'Eel, cucumber, avocado, eel sauce', 'price': 750, 'image': 'https://images.unsplash.com/photo-1564489563601-c53cfc451e93?w=400'},
                {'name': 'Salmon Nigiri (5pcs)', 'description': 'Fresh salmon over seasoned rice', 'price': 600, 'image': 'https://images.unsplash.com/photo-1617196034796-73dfa7b1fd56?w=400'},
            ],
            'Pasta & Italian': [
                {'name': 'Spaghetti Carbonara', 'description': 'Creamy sauce, pancetta, parmesan, black pepper', 'price': 550, 'image': 'https://images.unsplash.com/photo-1612874742237-6526221588e3?w=400'},
                {'name': 'Penne Arrabbiata', 'description': 'Spicy tomato sauce, garlic, chili flakes', 'price': 480, 'image': 'https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=400'},
                {'name': 'Fettuccine Alfredo', 'description': 'Rich cream sauce, parmesan, butter', 'price': 520, 'image': 'https://images.unsplash.com/photo-1645112411341-6c4fd023714a?w=400'},
                {'name': 'Lasagna Bolognese', 'description': 'Layered pasta, meat sauce, béchamel, cheese', 'price': 650, 'image': 'https://images.unsplash.com/photo-1574894709920-11b28e7367e3?w=400'},
            ],
            'Asian Cuisine': [
                {'name': 'Pad Thai', 'description': 'Stir-fried rice noodles, shrimp, peanuts, lime', 'price': 500, 'image': 'https://images.unsplash.com/photo-1559314809-0d155014e29e?w=400'},
                {'name': 'Chicken Fried Rice', 'description': 'Wok-fried rice, chicken, vegetables, soy sauce', 'price': 380, 'image': 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=400'},
                {'name': 'Beef Ramen', 'description': 'Rich broth, tender beef, noodles, soft-boiled egg', 'price': 580, 'image': 'https://images.unsplash.com/photo-1591814468924-caf88d1232e1?w=400'},
                {'name': 'Spring Rolls (6pcs)', 'description': 'Crispy rolls with vegetables, sweet chili sauce', 'price': 320, 'image': 'https://images.unsplash.com/photo-1620222071550-a5c7f8b600ed?w=400'},
            ],
            'Desserts': [
                {'name': 'Chocolate Lava Cake', 'description': 'Warm chocolate cake with molten center, vanilla ice cream', 'price': 350, 'image': 'https://images.unsplash.com/photo-1624353365286-3f8d62daad51?w=400'},
                {'name': 'Tiramisu', 'description': 'Coffee-soaked ladyfingers, mascarpone, cocoa', 'price': 380, 'image': 'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=400'},
                {'name': 'Cheesecake', 'description': 'New York style cheesecake with berry compote', 'price': 400, 'image': 'https://images.unsplash.com/photo-1533134242443-d4fd215305ad?w=400'},
                {'name': 'Ice Cream Sundae', 'description': 'Three scoops, chocolate sauce, whipped cream, cherry', 'price': 280, 'image': 'https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=400'},
            ],
            'Beverages': [
                {'name': 'Fresh Orange Juice', 'description': 'Freshly squeezed orange juice', 'price': 150, 'image': 'https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=400'},
                {'name': 'Mango Smoothie', 'description': 'Blended mango, yogurt, honey', 'price': 200, 'image': 'https://images.unsplash.com/photo-1505252585461-04db1eb84625?w=400'},
                {'name': 'Iced Coffee', 'description': 'Cold brew coffee with milk and ice', 'price': 180, 'image': 'https://images.unsplash.com/photo-1517487881594-2787fef5ebf7?w=400'},
                {'name': 'Green Tea', 'description': 'Premium Japanese green tea', 'price': 120, 'image': 'https://images.unsplash.com/photo-1564890369478-c89ca6d9cde9?w=400'},
            ],
        }

        created_count = 0
        
        for restaurant in restaurants:
            self.stdout.write(f'\nAdding items to {restaurant.name}...')
            
            # Add items from 3-4 random categories to each restaurant
            import random
            categories = random.sample(list(menu_data.keys()), min(4, len(menu_data)))
            
            for category in categories:
                items = menu_data[category]
                # Add 2-4 items from each category
                selected_items = random.sample(items, min(random.randint(2, 4), len(items)))
                
                for item_data in selected_items:
                    item, created = MenuItem.objects.get_or_create(
                        restaurant=restaurant,
                        name=item_data['name'],
                        defaults={
                            'description': item_data['description'],
                            'price': item_data['price'],
                            'image': item_data['image'],
                            'is_available': True
                        }
                    )
                    if created:
                        created_count += 1
                        self.stdout.write(self.style.SUCCESS(f'  ✓ Added: {item.name} - ৳{item.price}'))

        self.stdout.write(self.style.SUCCESS(f'\n✅ Successfully added {created_count} new menu items!'))
        self.stdout.write(self.style.SUCCESS(f'Total menu items now: {MenuItem.objects.count()}'))
