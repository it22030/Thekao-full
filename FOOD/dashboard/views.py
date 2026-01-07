from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db import models
from django.db.models import Sum

from orders.models import Order
from restaurants.models import Restaurant
from rides.models import Ride
from parcels.models import ParcelRequest
from mall.models import Shop, MallOrder

User = get_user_model()


# ======================
# ROLE CHECKS
# ======================

def is_admin(user):
    return user.is_authenticated and (user.role == 'admin' or user.is_superuser)

def is_rider(user):
    return user.is_authenticated and user.role == 'rider'

def rider_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('rider_login')
        if request.user.role != 'rider':
            messages.error(request, "Access Denied. Riders only.")
            return redirect('rider_login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


# ======================
# ADMIN DASHBOARD
# ======================

@login_required
@user_passes_test(is_admin)
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    context = {
        'total_users': User.objects.count(),
        'total_orders': Order.objects.count(),
        'total_restaurants': Restaurant.objects.count(),
        'total_riders': User.objects.filter(role='rider').count(),
        'total_revenue': Order.objects.filter(status='delivered').aggregate(total=Sum('total_price'))['total'] or 0,

        # Mall & Parcel Stats
        'total_shops': Shop.objects.count(),
        'total_mall_orders': MallOrder.objects.count(),
        'total_parcels': ParcelRequest.objects.count(),

        'active_orders': Order.objects.exclude(status__in=['delivered', 'cancelled']).count(),
        'completed_orders': Order.objects.filter(status='delivered').count(),
        'cancelled_orders': Order.objects.filter(status='cancelled').count(),

        'recent_orders': Order.objects.select_related('user').order_by('-created_at')[:5],
    }
    return render(request, 'dashboard/index.html', context)


@login_required
@user_passes_test(is_admin)
def manage_users(request):
    users = User.objects.all()
    return render(request, 'dashboard/user_list.html', {'users': users})


@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_superuser:
        messages.error(request, "You cannot delete a superuser.")
    else:
        user.delete()
        messages.success(request, f"User {user.username} deleted.")
    return redirect('manage_users')


@login_required
@user_passes_test(is_admin)
def manage_restaurants(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'dashboard/restaurant_list.html', {'restaurants': restaurants})


@login_required
@user_passes_test(is_admin)
def manage_orders(request):
    orders = Order.objects.select_related('user', 'rider').order_by('-created_at')
    # Only show food delivery riders (food or both)
    riders = User.objects.filter(
        role='rider'
    ).filter(
        models.Q(rider_profile__is_food_rider=True)
    )
    return render(request, 'dashboard/order_list.html', {
        'orders': orders,
        'riders': riders
    })


@login_required
@user_passes_test(is_admin)
def assign_rider(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        rider_id = request.POST.get('rider_id')

        if not rider_id:
            messages.error(request, "Please select a rider.")
            return redirect('order_detail', order_id=order.id)

        # Only allow assignment of food delivery riders
        rider = get_object_or_404(
            User,
            id=rider_id,
            role='rider',
            rider_profile__is_food_rider=True
        )

        order.rider = rider
        if order.status == 'placed':
            order.status = 'accepted'
        order.save()

        messages.success(
            request,
            f"Rider {rider.username} assigned to Order #{order.id}"
        )

    return redirect('order_detail', order_id=order.id)


@login_required
@user_passes_test(is_admin)
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'cancelled'
    order.save()
    messages.success(request, f"Order #{order.id} cancelled.")
    return redirect('manage_orders')


@login_required
@user_passes_test(is_admin)
def manage_riders(request):
    # Add filtering by rider type
    # Add filtering by rider type (custom filter logic)
    rider_type = request.GET.get('type', 'all')
    riders = User.objects.filter(role='rider').select_related('rider_profile')
    
    if rider_type == 'food':
        riders = riders.filter(rider_profile__is_food_rider=True)
    elif rider_type == 'parcel':
        riders = riders.filter(rider_profile__is_parcel_rider=True)
    elif rider_type == 'ride':
        riders = riders.filter(rider_profile__is_ride_rider=True)
    elif rider_type == 'both':
        # interpret 'both' as multiple services users, or specific combo
        riders = riders.filter(rider_profile__is_food_rider=True, rider_profile__is_parcel_rider=True)
    
    return render(request, 'dashboard/rider_list.html', {
        'riders': riders,
        'current_filter': rider_type
    })


@login_required
@user_passes_test(is_admin)
def manage_rides(request):
    rides = Ride.objects.select_related('passenger', 'driver').order_by('-created_at')
    riders = User.objects.filter(
        role='rider',
        rider_profile__is_ride_rider=True
    )
    return render(request, 'dashboard/ride_list.html', {
        'rides': rides,
        'riders': riders
    })


@login_required
@user_passes_test(is_admin)
def assign_ride(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id)

    if request.method == 'POST':
        driver_id = request.POST.get('driver_id')

        if not driver_id:
            messages.error(request, "Please select a driver.")
            return redirect('manage_rides')

        driver = get_object_or_404(
            User,
            id=driver_id,
            role='rider',
            rider_profile__is_ride_rider=True
        )

        ride.driver = driver
        if ride.status == 'requested':
            ride.status = 'accepted'
        ride.save()

        messages.success(
            request,
            f"Driver {driver.username} assigned to Ride #{ride.id}"
        )

    return redirect('manage_rides')


@login_required
@user_passes_test(is_admin)
def manage_shops(request):
    shops = Shop.objects.all()
    return render(request, 'dashboard/mall/shop_list.html', {'shops': shops})


@login_required
@user_passes_test(is_admin)
def manage_mall_orders(request):
    orders = MallOrder.objects.select_related('user').order_by('-created_at')
    return render(request, 'dashboard/mall/order_list.html', {'orders': orders})


@login_required
@user_passes_test(is_admin)
def manage_parcels(request):
    parcels = ParcelRequest.objects.select_related('sender', 'rider').order_by('-created_at')
    # Only show parcel delivery riders (parcel or both)
    riders = User.objects.filter(
        role='rider',
        rider_profile__is_parcel_rider=True
    )
    return render(request, 'dashboard/parcels/parcel_list.html', {
        'parcels': parcels,
        'riders': riders
    })


@login_required
@user_passes_test(is_admin)
def assign_parcel_rider(request, parcel_id):
    parcel = get_object_or_404(ParcelRequest, id=parcel_id)
    
    if request.method == 'POST':
        rider_id = request.POST.get('rider_id')
        
        if not rider_id:
            messages.error(request, "Please select a rider.")
            return redirect('manage_parcels')
        
        # Only allow assignment of parcel delivery riders
        rider = get_object_or_404(
            User,
            id=rider_id,
            role='rider',
            rider_profile__is_parcel_rider=True
        )
        
        parcel.rider = rider
        if parcel.status == 'requested':
            parcel.status = 'accepted'
        parcel.save()
        
        messages.success(
            request,
            f"Rider {rider.username} assigned to Parcel #{parcel.tracking_number}"
        )
    
    return redirect('manage_parcels')



@login_required
@user_passes_test(is_admin)
def add_restaurant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        address = request.POST.get('address')
        image = request.POST.get('image')
        
        Restaurant.objects.create(
            name=name,
            description=description,
            address=address,
            image=image
        )
        messages.success(request, f"Restaurant '{name}' added successfully.")
        return redirect('manage_restaurants')
    
    return render(request, 'dashboard/add_restaurant.html')


@login_required
@user_passes_test(is_admin)
def delete_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    name = restaurant.name
    restaurant.delete()
    messages.success(request, f"Restaurant '{name}' deleted successfully.")
    return redirect('manage_restaurants')


@login_required
@user_passes_test(is_admin)
def manage_settings(request):
    from core.models import GlobalSettings
    settings = GlobalSettings.load()
    
    if request.method == 'POST':
        try:
            # Food
            settings.food_delivery_charge = request.POST.get('food_delivery_charge')
            settings.food_commission_percentage = request.POST.get('food_commission')
            
            # Rides
            settings.ride_commission_percentage = request.POST.get('ride_commission')
            
            # Parcels
            settings.parcel_commission_percentage = request.POST.get('parcel_commission')
            
            # Mall
            settings.mall_commission_percentage = request.POST.get('mall_commission')
            
            settings.save()
            messages.success(request, "Global settings updated.")
        except Exception as e:
            messages.error(request, f"Error updating settings: {e}")
            
    # Calculate example breakdowns
    example_total = 100
    
    context = {
        'settings': settings,
        'example_total': example_total,
        'food_rider_cut': (example_total * settings.food_commission_percentage) / 100,
        'ride_driver_cut': (example_total * settings.ride_commission_percentage) / 100,
        'parcel_rider_cut': (example_total * settings.parcel_commission_percentage) / 100,
        'mall_platform_cut': (example_total * settings.mall_commission_percentage) / 100,
    }
            
    return render(request, 'dashboard/settings.html', context)


@login_required
@user_passes_test(is_admin)
def update_rider_services(request, rider_id):
    rider = get_object_or_404(User, id=rider_id, role='rider')
    profile = rider.rider_profile
    
    if request.method == 'POST':
        profile.is_food_rider = 'is_food_rider' in request.POST
        profile.is_parcel_rider = 'is_parcel_rider' in request.POST
        profile.is_ride_rider = 'is_ride_rider' in request.POST
        profile.save()
        messages.success(request, f"Services updated for {rider.username}")
        
    return redirect('manage_riders')


# ======================
# RIDER DASHBOARD
# ======================

@rider_required
def rider_dashboard(request):
    rider_profile = getattr(request.user, 'rider_profile', None)
    
    # --- ACTIVE TASKS (Assigned to this rider) ---
    active_tasks = []

    # 1. Food Orders
    if rider_profile and rider_profile.is_food_rider:
        food_orders = Order.objects.filter(rider=request.user).exclude(status__in=['delivered', 'cancelled']).order_by('-created_at')
        for o in food_orders:
            active_tasks.append({
                'id': o.id, 'type': 'food', 'icon': '🍔', 'title': f"Food Order #{o.id}",
                'customer': o.user.get_full_name() or o.user.username, 'status': o.get_status_display(),
                'raw_status': o.status, 'total': o.total_price, 'fee': o.rider_fee, 'url': f"/dashboard/orders/{o.id}/"
            })

    # 2. Mall Orders
    if rider_profile and rider_profile.is_food_rider: # Mall often uses food riders
        mall_orders = MallOrder.objects.filter(rider=request.user).exclude(status__in=['delivered', 'cancelled']).order_by('-created_at')
        for o in mall_orders:
            active_tasks.append({
                'id': o.id, 'type': 'mall', 'icon': '🛍️', 'title': f"Mall Order #{o.id}",
                'customer': o.user.get_full_name() or o.user.username, 'status': o.get_status_display(),
                'raw_status': o.status, 'total': o.total_price, 'fee': o.rider_fee, 'url': f"/dashboard/mall/orders/{o.id}/" # Assuming URL
            })

    # 3. Parcels
    if rider_profile and rider_profile.is_parcel_rider:
        parcels = ParcelRequest.objects.filter(rider=request.user, status__in=['accepted', 'picked_up']).order_by('-created_at')
        for p in parcels:
            active_tasks.append({
                'id': p.id, 'type': 'parcel', 'icon': '📦', 'title': f"Parcel #{p.tracking_number}",
                'customer': p.receiver_name, 'status': p.get_status_display(),
                'raw_status': p.status, 'total': p.price, 'fee': p.rider_fee, 'url': f"/parcels/detail/{p.id}/"
            })

    # 4. Rides
    if rider_profile and rider_profile.is_ride_rider:
        rides = Ride.objects.filter(driver=request.user, status__in=['accepted', 'in_progress']).order_by('-created_at')
        for r in rides:
            active_tasks.append({
                'id': r.id, 'type': 'ride', 'icon': '🚗', 'title': f"Ride Request #{r.id}",
                'customer': r.passenger.get_full_name() or r.passenger.username, 'status': r.get_status_display(),
                'raw_status': r.status, 'total': r.fare, 'fee': r.rider_fee, 'url': f"/rides/ride/{r.id}/"
            })

    # --- AVAILABLE TASKS (Not yet assigned) ---
    available_tasks = []

    if rider_profile:
        if rider_profile.is_food_rider:
            # Available Food
            for o in Order.objects.filter(rider__isnull=True, status='placed'):
                available_tasks.append({'id': o.id, 'type': 'food', 'icon': '🍔', 'title': f"Available Food #{o.id}", 'total': o.total_price, 'fee': o.rider_fee, 'accept_url': f"/dashboard/rider/accept-order/{o.id}/"})
            # Available Mall
            for o in MallOrder.objects.filter(rider__isnull=True, status='placed'):
                available_tasks.append({'id': o.id, 'type': 'mall', 'icon': '🛍️', 'title': f"Available Mall #{o.id}", 'total': o.total_price, 'fee': o.rider_fee, 'accept_url': f"/dashboard/rider/mall-accept/{o.id}/"})
        
        if rider_profile.is_parcel_rider:
            for p in ParcelRequest.objects.filter(rider__isnull=True, status='requested'):
                available_tasks.append({'id': p.id, 'type': 'parcel', 'icon': '📦', 'title': f"Available Parcel #{p.tracking_number}", 'total': p.price, 'fee': p.rider_fee, 'accept_url': f"/parcels/accept/{p.id}/"})
        
        if rider_profile.is_ride_rider:
            for r in Ride.objects.filter(driver__isnull=True, status='requested'):
                available_tasks.append({'id': r.id, 'type': 'ride', 'icon': '🚗', 'title': f"Available Ride #{r.id}", 'total': r.fare, 'fee': r.rider_fee, 'accept_url': f"/rides/accept/{r.id}/"})

    # --- EARNINGS & STATS ---
    food_earnings = Order.objects.filter(rider=request.user, status='delivered').aggregate(total=Sum('rider_fee'))['total'] or 0
    mall_earnings = MallOrder.objects.filter(rider=request.user, status='delivered').aggregate(total=Sum('rider_fee'))['total'] or 0
    parcel_earnings = ParcelRequest.objects.filter(rider=request.user, status='delivered').aggregate(total=Sum('rider_fee'))['total'] or 0
    ride_earnings = Ride.objects.filter(driver=request.user, status='completed').aggregate(total=Sum('rider_fee'))['total'] or 0
    
    total_earnings = food_earnings + mall_earnings + parcel_earnings + ride_earnings

    context = {
        'rider': request.user,
        'profile': rider_profile,
        'total_earnings': total_earnings,
        'food_earnings': food_earnings,
        'mall_earnings': mall_earnings,
        'parcel_earnings': parcel_earnings,
        'ride_earnings': ride_earnings,
        'active_tasks': active_tasks,
        'available_tasks': available_tasks,
        'completed_count': (
            Order.objects.filter(rider=request.user, status='delivered').count() +
            MallOrder.objects.filter(rider=request.user, status='delivered').count() +
            ParcelRequest.objects.filter(rider=request.user, status='delivered').count() +
            Ride.objects.filter(driver=request.user, status='completed').count()
        )
    }
    return render(request, 'dashboard/rider_dashboard.html', context)


@rider_required
def available_orders(request):
    # Only show available orders to food delivery riders
    rider_profile = getattr(request.user, 'rider_profile', None)
    if not rider_profile or not rider_profile.is_food_rider:
        messages.error(request, "You are not registered for food delivery service.")
        return redirect('rider_dashboard')
    
    orders = Order.objects.filter(
        rider__isnull=True,
        status='placed'
    ).order_by('-created_at')

    return render(request, 'dashboard/available_orders.html', {'orders': orders})


@rider_required
def accept_order(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        rider__isnull=True,
        status='placed'
    )

    order.rider = request.user
    order.status = 'accepted'
    order.save()

    messages.success(request, f"Order #{order.id} accepted.")
    return redirect('rider_dashboard')


@rider_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id, rider=request.user)

    if request.method == 'POST':
        new_status = request.POST.get('status')

        allowed = ['accepted', 'preparing', 'out_for_delivery', 'delivered']
        if new_status in allowed:
            order.status = new_status
            order.save()
            messages.success(
                request,
                f"Order #{order.id} marked as {order.get_status_display()}."
            )
        else:
            messages.error(request, "Invalid status update.")

    next_url = request.POST.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('rider_dashboard')


# ======================
# MALL RIDER VIEWS
# ======================

@rider_required
def available_mall_orders(request):
    orders = MallOrder.objects.filter(
        rider__isnull=True,
        status='placed'
    ).order_by('-created_at')

    return render(request, 'dashboard/mall/available_orders.html', {'orders': orders})


@rider_required
def accept_mall_order(request, order_id):
    order = get_object_or_404(
        MallOrder,
        id=order_id,
        rider__isnull=True,
        status='placed'
    )

    order.rider = request.user
    order.status = 'accepted'
    order.save()

    messages.success(request, f"Mall Order #{order.id} accepted.")
    return redirect('rider_dashboard')


@rider_required
def update_mall_order_status(request, order_id):
    order = get_object_or_404(MallOrder, id=order_id, rider=request.user)

    if request.method == 'POST':
        new_status = request.POST.get('status')

        allowed = ['confirmed', 'shipped', 'picked_up', 'delivered']
        if new_status in allowed:
            order.status = new_status
            order.save()
            messages.success(
                request,
                f"Mall Order #{order.id} marked as {order.get_status_display()}."
            )
        else:
            messages.error(request, "Invalid status update.")

    return redirect('rider_dashboard')
