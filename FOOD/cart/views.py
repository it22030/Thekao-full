from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from menu.models import MenuItem

def _get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = request.session.get('cart_id')
        if cart_id:
            try:
                cart = Cart.objects.get(id=cart_id)
            except Cart.DoesNotExist:
                cart = Cart.objects.create()
                request.session['cart_id'] = cart.id
        else:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
    return cart

def add_to_cart(request, item_id):
    cart = _get_cart(request)
    item = get_object_or_404(MenuItem, id=item_id)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart_detail')

def remove_from_cart(request, item_id):
    cart = _get_cart(request)
    item = get_object_or_404(MenuItem, id=item_id)
    
    # Logic to remove or decrement? Let's just remove for simplicity or decrement
    # For now, let's just remove logic is better on Detail page usually
    # But wait, request handler.
    try:
        cart_item = CartItem.objects.get(cart=cart, menu_item=item)
        if cart_item:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass

    return redirect('cart_detail')

def cart_detail(request):
    cart = _get_cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})
