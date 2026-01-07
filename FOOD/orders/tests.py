from django.test import TestCase
from django.contrib.auth import get_user_model
from orders.models import Order
from menu.models import MenuItem, Restaurant

User = get_user_model()

class OrderStatusTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='customer', password='password')
        self.rider = User.objects.create_user(username='rider', password='password', role='rider')
        self.restaurant = Restaurant.objects.create(name="Test Rest", address="Address")
        self.item = MenuItem.objects.create(restaurant=self.restaurant, name='Pizza', price=10.00)

    def test_order_creation_with_delivery_details(self):
        order = Order.objects.create(
            user=self.user,
            total_price=10.00,
            delivery_address="123 Test St",
            customer_phone="555-1234"
        )
        self.assertEqual(order.delivery_address, "123 Test St")
        self.assertEqual(order.customer_phone, "555-1234")
        self.assertEqual(order.status, 'placed')

    def test_rider_status_update(self):
        order = Order.objects.create(
            user=self.user,
            total_price=10.00,
            rider=self.rider,
            status='accepted'
        )
        
        # Simulate status update by rider
        order.status = 'preparing'
        order.save()
        self.assertEqual(order.status, 'preparing')
        
        order.status = 'out_for_delivery'
        order.save()
        self.assertEqual(order.status, 'out_for_delivery')
        
        order.status = 'delivered'
        order.save()
        self.assertEqual(order.status, 'delivered')
