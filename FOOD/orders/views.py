from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from cart.models import Cart


def create_order(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        user = request.user if request.user.is_authenticated else None
        
        # If no user, we might want to fail or use a demo user. 
        # For now, if no user, redirect to login (which likely doesn't exist, so we'll just handle gracefully or fail).
        if not user:
             # Just for demo: if no user loggged in, we create anonymous order if possible or just error.
             # Ideally we should redirect to login.
             # return redirect('/accounts/login/?next=/')
             pass

        if user:
            from menu.models import MenuItem
            delivery_address = request.POST.get('delivery_address', '')
            customer_phone = request.POST.get('customer_phone', '')
            
            order = Order.objects.create(
                user=user, 
                total_price=total_price, 
                status='placed',
                delivery_address=delivery_address,
                customer_phone=customer_phone
            )
            
            if item_id:
                try:
                    item = MenuItem.objects.get(id=item_id)
                    OrderItem.objects.create(
                        order=order,
                        menu_item=item,
                        quantity=1,
                        price=item.price
                    )
                except MenuItem.DoesNotExist:
                    pass

            return redirect('order_detail', order_id=order.id)
    return render(request, 'orders/create_order.html')

def create_order_from_cart(request):
    if request.method == 'POST':
        # Retrieve cart
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            cart_id = request.session.get('cart_id')
            if cart_id:
                cart = Cart.objects.filter(id=cart_id).first()
            else:
                cart = None
        
        if not cart or not cart.items.exists():
            return redirect('cart_detail')
            
        # Create Order
        user = request.user if request.user.is_authenticated else None
        
        # This is a bit loose on the User constraint defined in models.py (which requires user).
        # We will require login for checkout or assign a "guest" user if we had one.
        # For this requirement, let's enforce login for checkout if user is None.
        if not user:
             return redirect('/accounts/login/?next=/cart/')

        delivery_address = request.POST.get('delivery_address', '')
        customer_phone = request.POST.get('customer_phone', '')

        total_price = cart.get_total_price()
        order = Order.objects.create(
            user=user, 
            total_price=total_price, 
            status='placed',
            delivery_address=delivery_address,
            customer_phone=customer_phone
        )
        
        # Copy items from cart to order
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                menu_item=cart_item.menu_item,
                quantity=cart_item.quantity,
                price=cart_item.menu_item.price
            )
            
        # Clearing cart
        cart.items.all().delete()
        
        return redirect('order_detail', order_id=order.id)
    return redirect('cart_detail')

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    template = 'orders/order_detail.html'
    
    context = {'order': order}
    
    # Use dashboard-themed template for staff (admins and riders)
    if request.user.is_authenticated and (request.user.role in ['admin', 'rider'] or request.user.is_superuser):
        template = 'dashboard/order_detail.html'
        if request.user.role == 'admin' or request.user.is_superuser:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            context['riders'] = User.objects.filter(role='rider')
        
    return render(request, template, context)
