from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class ParcelRequest(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('picked_up', 'Picked Up'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    sender = models.ForeignKey(User, related_name='sent_parcels', on_delete=models.CASCADE)
    rider = models.ForeignKey(User, related_name='delivered_parcels', null=True, blank=True, on_delete=models.SET_NULL)
    
    pickup_address = models.CharField(max_length=255)
    dropoff_address = models.CharField(max_length=255)
    
    receiver_name = models.CharField(max_length=100)
    receiver_phone = models.CharField(max_length=20)
    
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in KG")
    description = models.TextField(blank=True, help_text="What's in the package?")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    
    tracking_number = models.CharField(max_length=50, unique=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    rider_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    platform_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if not self.tracking_number:
            import uuid
            self.tracking_number = str(uuid.uuid4()).split('-')[0].upper()
            
        if self.price and not self.rider_fee:
            from core.models import GlobalSettings
            settings = GlobalSettings.load()
            
            # Calculate Rider Fee
            commission = settings.parcel_commission_percentage
            self.rider_fee = (self.price * commission) / 100
            self.platform_profit = self.price - self.rider_fee

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Parcel #{self.tracking_number} to {self.receiver_name}"
