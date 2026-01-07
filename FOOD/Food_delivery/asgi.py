import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from orders.routing import websocket_urlpatterns as order_ws_urls
from mall.routing import websocket_urlpatterns as mall_ws_urls
from dashboard.routing import websocket_urlpatterns as dashboard_ws_urls

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Food_delivery.settings')

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": URLRouter(
      order_ws_urls + mall_ws_urls + dashboard_ws_urls
  ),
})
