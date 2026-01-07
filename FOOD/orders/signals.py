from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=Order)
def order_status_changed(sender, instance, created, **kwargs):
    if not created:
        channel_layer = get_channel_layer()
        data = {
            'type': 'task_update',
            'data': {
                'status': instance.get_status_display(),
                'raw_status': instance.status,
                'rider_name': instance.rider.username if instance.rider else None,
                'order_id': instance.id,
            }
        }
        # Unified group
        async_to_sync(channel_layer.group_send)(
            f"task_food_{instance.id}",
            data
        )
        
        # Legacy groups
        async_to_sync(channel_layer.group_send)(
            f"order_{instance.id}",
            {
                'type': 'order_status_update',
                'status': instance.get_status_display(),
                'rider_name': instance.rider.username if instance.rider else None,
                'order_id': instance.id,
            }
        )
        async_to_sync(channel_layer.group_send)(
            "orders",
            {
                "type": "order_update",
                "message": {
                    'status': instance.get_status_display(),
                    'rider_name': instance.rider.username if instance.rider else None,
                    'order_id': instance.id,
                }
            }
        )
