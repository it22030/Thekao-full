from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ParcelRequest
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=ParcelRequest)
def parcel_status_handler(sender, instance, created, **kwargs):
    if not created:
        channel_layer = get_channel_layer()
        data = {
            'type': 'task_update',
            'data': {
                'status': instance.get_status_display(),
                'raw_status': instance.status,
                'rider_name': instance.rider.username if instance.rider else None,
            }
        }
        # Send to the new unified group
        async_to_sync(channel_layer.group_send)(
            f"task_parcel_{instance.id}",
            data
        )
