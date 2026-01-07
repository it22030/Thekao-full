from django.core.management.base import BaseCommand
from mall.models import Shop, Product


class Command(BaseCommand):
    help = 'Seed the database with sample shops and products'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding mall data...')
        
        # Clear existing data
        Product.objects.all().delete()
        Shop.objects.all().delete()
        
        # Create Shops
        shops_data = [
            {
                'name': 'TechZone Electronics',
                'description': 'Your one-stop shop for the latest gadgets and electronics',
                'address': 'Dhanmondi, Dhaka',
                'image': 'https://images.unsplash.com/photo-1498049794561-7780e7231661?w=800'
            },
            {
                'name': 'Fashion Hub',
                'description': 'Trendy clothing and accessories for everyone',
                'address': 'Gulshan, Dhaka',
                'image': 'https://images.unsplash.com/photo-1441984904996-e0b6ba687e04?w=800'
            },
            {
                'name': 'Home & Living',
                'description': 'Beautiful furniture and home decor items',
                'address': 'Banani, Dhaka',
                'image': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800'
            },
            {
                'name': 'Sports Corner',
                'description': 'Premium sports equipment and fitness gear',
                'address': 'Mirpur, Dhaka',
                'image': 'https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=800'
            },
        ]
        
        shops = {}
        for shop_data in shops_data:
            shop = Shop.objects.create(**shop_data)
            shops[shop.name] = shop
            self.stdout.write(f'Created shop: {shop.name}')
        
        # Create Products for TechZone Electronics
        tech_products = [
            {'name': 'Wireless Headphones', 'price': 4500, 'stock': 25, 'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400'},
            {'name': 'Smart Watch', 'price': 8500, 'stock': 15, 'image': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400'},
            {'name': 'Bluetooth Speaker', 'price': 3200, 'stock': 30, 'image': 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400'},
            {'name': 'Laptop Stand', 'price': 1800, 'stock': 40, 'image': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400'},
            {'name': 'USB-C Hub', 'price': 2500, 'stock': 35, 'image': 'https://images.unsplash.com/photo-1625948515291-69613efd103f?w=400'},
        ]
        
        for product_data in tech_products:
            Product.objects.create(
                shop=shops['TechZone Electronics'],
                description=f'High-quality {product_data["name"]} with warranty',
                **product_data
            )
        
        # Create Products for Fashion Hub
        fashion_products = [
            {'name': 'Casual T-Shirt', 'price': 850, 'stock': 50, 'image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400'},
            {'name': 'Denim Jeans', 'price': 2200, 'stock': 30, 'image': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400'},
            {'name': 'Leather Jacket', 'price': 5500, 'stock': 12, 'image': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400'},
            {'name': 'Sneakers', 'price': 3800, 'stock': 25, 'image': 'https://images.unsplash.com/photo-1460353581641-37baddab0fa2?w=400'},
            {'name': 'Backpack', 'price': 1950, 'stock': 40, 'image': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400'},
        ]
        
        for product_data in fashion_products:
            Product.objects.create(
                shop=shops['Fashion Hub'],
                description=f'Stylish {product_data["name"]} for modern lifestyle',
                **product_data
            )
        
        # Create Products for Home & Living
        home_products = [
            {'name': 'Table Lamp', 'price': 1650, 'stock': 20, 'image': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400'},
            {'name': 'Wall Clock', 'price': 1200, 'stock': 30, 'image': 'https://images.unsplash.com/photo-1563861826100-9cb868fdbe1c?w=400'},
            {'name': 'Cushion Set', 'price': 2100, 'stock': 25, 'image': 'https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=400'},
            {'name': 'Plant Pot', 'price': 850, 'stock': 45, 'image': 'https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=400'},
            {'name': 'Throw Blanket', 'price': 1850, 'stock': 18, 'image': 'https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=400'},
        ]
        
        for product_data in home_products:
            Product.objects.create(
                shop=shops['Home & Living'],
                description=f'Beautiful {product_data["name"]} for your home',
                **product_data
            )
        
        # Create Products for Sports Corner
        sports_products = [
            {'name': 'Yoga Mat', 'price': 1450, 'stock': 35, 'image': 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400'},
            {'name': 'Dumbbell Set', 'price': 3500, 'stock': 20, 'image': 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400'},
            {'name': 'Running Shoes', 'price': 4200, 'stock': 28, 'image': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400'},
            {'name': 'Water Bottle', 'price': 650, 'stock': 60, 'image': 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400'},
            {'name': 'Resistance Bands', 'price': 1100, 'stock': 40, 'image': 'https://images.unsplash.com/photo-1598289431512-b97b0917affc?w=400'},
        ]
        
        for product_data in sports_products:
            Product.objects.create(
                shop=shops['Sports Corner'],
                description=f'Professional {product_data["name"]} for fitness enthusiasts',
                **product_data
            )
        
        total_products = Product.objects.count()
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(shops)} shops and {total_products} products!'))
