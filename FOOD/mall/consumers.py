import json
from channels.generic.websocket import AsyncWebsocketConsumer

class MallOrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self.order_group_name = 'mall_order_%s' % self.order_id

        # Join room group
        await self.channel_layer.group_add(
            self.order_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.order_group_name,
            self.channel_name
        )

    # Receive message from room group
    async def mall_order_update(self, event):
        status = event['status']
        rider_name = event.get('rider_name', None)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'status': status,
            'rider_name': rider_name
        }))
