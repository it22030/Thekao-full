from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Shop, Product, MallOrder, MallOrderItem

def mall_home(request):
    shops = Shop.objects.all()
    return render(request, 'mall/home.html', {'shops': shops})

def shop_detail(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)
    products = shop.products.filter(is_available=True)
    return render(request, 'mall/shop_detail.html', {'shop': shop, 'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'mall/product_detail.html', {'product': product})

# ==================
# SHOPPING CART
# ==================

def get_mall_cart(request):
    """Get or initialize mall cart from session"""
    cart = request.session.get('mall_cart', {})
    return cart

def save_mall_cart(request, cart):
    """Save mall cart to session"""
    request.session['mall_cart'] = cart
    request.session.modified = True

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if not product.is_available or product.stock < 1:
        messages.error(request, f"{product.name} is currently out of stock.")
        return redirect('shop_detail', shop_id=product.shop.id)
    
    cart = get_mall_cart(request)
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        # Check stock before incrementing
        if cart[product_id_str]['quantity'] < product.stock:
            cart[product_id_str]['quantity'] += 1
            messages.success(request, f"Added another {product.name} to cart.")
        else:
            messages.warning(request, f"Cannot add more. Only {product.stock} in stock.")
    else:
        cart[product_id_str] = {
            'product_id': product.id,
            'name': product.name,
            'price': str(product.price),
            'quantity': 1,
            'shop_name': product.shop.name,
            'image': product.image
        }
        messages.success(request, f"Added {product.name} to cart.")
    
    save_mall_cart(request, cart)
    return redirect(request.META.get('HTTP_REFERER', 'mall_home'))

@login_required
def view_cart(request):
    cart = get_mall_cart(request)
    cart_items = []
    total = 0
    
    for product_id, item in cart.items():
        subtotal = float(item['price']) * item['quantity']
        cart_items.append({
            'product_id': product_id,
            'name': item['name'],
            'price': float(item['price']),
            'quantity': item['quantity'],
            'subtotal': subtotal,
            'shop_name': item['shop_name'],
            'image': item.get('image', '')
        })
        total += subtotal
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'cart_count': sum(item['quantity'] for item in cart.values())
    }
    return render(request, 'mall/cart.html', context)

@login_required
def update_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = get_mall_cart(request)
        product_id_str = str(product_id)
        
        if product_id_str in cart:
            product = get_object_or_404(Product, id=product_id)
            
            if quantity > 0 and quantity <= product.stock:
                cart[product_id_str]['quantity'] = quantity
                messages.success(request, "Cart updated.")
            elif quantity > product.stock:
                messages.error(request, f"Only {product.stock} items available.")
            else:
                del cart[product_id_str]
                messages.success(request, "Item removed from cart.")
            
            save_mall_cart(request, cart)
    
    return redirect('mall_cart')

@login_required
def remove_from_cart(request, product_id):
    cart = get_mall_cart(request)
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        product_name = cart[product_id_str]['name']
        del cart[product_id_str]
        save_mall_cart(request, cart)
        messages.success(request, f"Removed {product_name} from cart.")
    
    return redirect('mall_cart')

# ==================
# CHECKOUT & ORDERS
# ==================

@login_required
def checkout(request):
    cart = get_mall_cart(request)
    
    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('mall_home')
    
    if request.method == 'POST':
        delivery_address = request.POST.get('delivery_address', '').strip()
        
        if not delivery_address:
            messages.error(request, "Please provide a delivery address.")
            return redirect('mall_checkout')
        
        # Calculate total
        total = sum(float(item['price']) * item['quantity'] for item in cart.values())
        
        # Create order
        order = MallOrder.objects.create(
            user=request.user,
            total_price=total,
            delivery_address=delivery_address,
            status='placed'
        )
        
        # Create order items and update stock
        for product_id, item in cart.items():
            product = Product.objects.get(id=product_id)
            MallOrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                price=item['price']
            )
            # Update stock
            product.stock -= item['quantity']
            product.save()
        
        # Clear cart
        request.session['mall_cart'] = {}
        request.session.modified = True
        
        messages.success(request, f"Order #{order.id} placed successfully!")
        return redirect('mall_order_detail', order_id=order.id)
    
    # GET request - show checkout form
    cart_items = []
    total = 0
    
    for product_id, item in cart.items():
        subtotal = float(item['price']) * item['quantity']
        cart_items.append({
            'name': item['name'],
            'price': float(item['price']),
            'quantity': item['quantity'],
            'subtotal': subtotal
        })
        total += subtotal
    
    context = {
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'mall/checkout.html', context)

@login_required
def my_mall_orders(request):
    orders = MallOrder.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'mall/my_orders.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(MallOrder, id=order_id, user=request.user)
    return render(request, 'mall/order_detail.html', {'order': order})
