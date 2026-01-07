from django.db import models

class GlobalSettings(models.Model):
    # Singleton pattern helper
    def save(self, *args, **kwargs):
        self.pk = 1
        super(GlobalSettings, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    # Food Delivery
    food_delivery_charge = models.DecimalField(max_digits=6, decimal_places=2, default=50.00)
    food_commission_percentage = models.PositiveIntegerField(default=80, help_text="Food: % of delivery fee for rider")

    # Rides
    ride_commission_percentage = models.PositiveIntegerField(default=80, help_text="Rides: % of fare for driver")

    # Parcels
    parcel_commission_percentage = models.PositiveIntegerField(default=80, help_text="Parcels: % of price for rider")

    # Mall
    mall_commission_percentage = models.PositiveIntegerField(default=10, help_text="Mall: % of order total for platform (rest to shop)")

    def __str__(self):
        return "Global Settings"
