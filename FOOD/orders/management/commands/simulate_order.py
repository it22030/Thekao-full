import time
from django.core.management.base import BaseCommand
from orders.models import Order

class Command(BaseCommand):
    help = 'Simulates an order lifecycle by updating its status every few seconds'

    def add_arguments(self, parser):
        parser.add_argument('order_id', type=int, help='The ID of the order to simulate')

    def handle(self, *args, **options):
        order_id = options['order_id']
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Order "{order_id}" does not exist'))
            return

        statuses = ['placed', 'accepted', 'preparing', 'out_for_delivery', 'delivered']
        
        self.stdout.write(self.style.SUCCESS(f'Starting simulation for Order #{order_id}'))

        for status in statuses:
            order.status = status
            order.save()
            self.stdout.write(f'Order #{order_id} status updated to: {status}')
            if status == 'delivered':
                break
            time.sleep(5)
            
        self.stdout.write(self.style.SUCCESS(f'Simulation complete for Order #{order_id}'))
