from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MallOrder
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=MallOrder)
def mall_order_status_handler(sender, instance, created, **kwargs):
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
        async_to_sync(channel_layer.group_send)(
            f"task_mall_{instance.id}",
            data
        )
        # Keep old group for backward compatibility if any template still uses it
        async_to_sync(channel_layer.group_send)(
            f"mall_order_{instance.id}",
            {
                'type': 'mall_order_update',
                'status': instance.get_status_display(),
                'rider_name': instance.rider.username if instance.rider else None,
                'order_id': instance.id,
            }
        )
