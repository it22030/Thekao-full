from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('restaurant', 'Restaurant'),
        ('admin', 'Admin'),
        ('rider', 'Rider'),
        ('seller', 'Seller'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='customer'
    )


class RiderProfile(models.Model):


    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='rider_profile'
    )
    phone_number = models.CharField(max_length=15, blank=True)
    # Service Flags
    is_food_rider = models.BooleanField(default=False, verbose_name="Food Delivery")
    is_parcel_rider = models.BooleanField(default=False, verbose_name="Parcel Delivery")
    is_ride_rider = models.BooleanField(default=False, verbose_name="Ride Sharing")
    
    # Keeping vehicle type and other info
    vehicle_type = models.CharField(max_length=50, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        services = []
        if self.is_food_rider: services.append("Food")
        if self.is_parcel_rider: services.append("Parcel")
        if self.is_ride_rider: services.append("Ride")
        return f"Rider: {self.user.username} ({', '.join(services)})"


@receiver(post_save, sender=User)
def ensure_rider_profile(sender, instance, **kwargs):
    """
    Ensure RiderProfile exists whenever a user is a rider.
    Handles:
    - new rider creation
    - role changed to rider later
    """
    if instance.role == 'rider':
        RiderProfile.objects.get_or_create(user=instance)
