from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Shop(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.URLField(max_length=500, blank=True)
    address = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    shop = models.ForeignKey(Shop, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(max_length=500, blank=True)
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} (${self.price})"

class MallOrder(models.Model):
    STATUS_CHOICES = [
        ('placed', 'Placed'),
        ('accepted', 'Accepted'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('picked_up', 'Picked Up'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rider = models.ForeignKey(User, related_name='mall_deliveries', null=True, blank=True, on_delete=models.SET_NULL)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='placed')
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_address = models.CharField(max_length=255)

    # Financials
    platform_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shop_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    rider_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if self.total_price and not self.platform_profit:
            from core.models import GlobalSettings
            settings = GlobalSettings.load()
            
            # Mall Commission: Platform takes X%, rest goes to shop
            commission = settings.mall_commission_percentage
            self.platform_profit = (self.total_price * commission) / 100
            self.shop_profit = self.total_price - self.platform_profit
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"MallOrder #{self.id}"

class MallOrderItem(models.Model):
    order = models.ForeignKey(MallOrder, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Snapshot of price

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
