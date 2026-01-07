from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class Order(models.Model):

    STATUS_CHOICES = [
        ('placed', 'Placed'),
        ('accepted', 'Accepted'),
        ('preparing', 'Preparing'),
        ('out_for_delivery', 'Out for delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rider = models.ForeignKey(User, related_name='deliveries', null=True, blank=True, on_delete=models.SET_NULL)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    
    # Pricing Breakdown
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    rider_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    platform_profit = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='placed'
    )
    delivery_address = models.CharField(max_length=255, blank=True)
    customer_phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.delivery_fee:
            from core.models import GlobalSettings
            settings = GlobalSettings.load()
            self.delivery_fee = settings.food_delivery_charge
            
            # Calculate Rider Fee
            commission = settings.food_commission_percentage
            self.rider_fee = (self.delivery_fee * commission) / 100
            self.platform_profit = self.delivery_fee - self.rider_fee
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey('menu.MenuItem', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} (Order #{self.order.id})"

    def get_cost(self):
        return self.price * self.quantity



# Signal handler removed. Logic consolidated in orders/signals.py
