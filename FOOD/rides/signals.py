from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import DriverLocation, Ride
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

User = settings.AUTH_USER_MODEL

@receiver(post_save, sender=User)
def create_driver_location(sender, instance, created, **kwargs):
    """
    Ensure every Rider has a DriverLocation instance.
    """
    if instance.role == 'rider':
        DriverLocation.objects.get_or_create(
            driver=instance,
            defaults={'lat': 23.8103, 'lng': 90.4125} # Default to Dhaka
        )

@receiver(post_save, sender=Ride)
def ride_status_handler(sender, instance, created, **kwargs):
    if not created:
        channel_layer = get_channel_layer()
        data = {
            'type': 'task_update',
            'data': {
                'status': instance.get_status_display(),
                'raw_status': instance.status,
                'driver_name': instance.driver.get_full_name() or instance.driver.username if instance.driver else "Waiting for driver",
            }
        }
        async_to_sync(channel_layer.group_send)(
            f"task_ride_{instance.id}",
            data
        )
