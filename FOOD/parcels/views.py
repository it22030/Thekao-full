from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ParcelRequest
from .forms import ParcelRequestForm

@login_required
def parcel_home(request):
    my_parcels = ParcelRequest.objects.filter(sender=request.user).order_by('-created_at')
    return render(request, 'parcels/home.html', {'my_parcels': my_parcels})

@login_required
def create_parcel(request):
    if request.method == 'POST':
        form = ParcelRequestForm(request.POST)
        if form.is_valid():
            parcel = form.save(commit=False)
            parcel.sender = request.user
            parcel.status = 'requested'
            # Calculate Price: Base $10 + $2 per kg
            parcel.price = 10 + (parcel.weight_kg * 2)
            parcel.save()
            return redirect('parcel_detail', parcel_id=parcel.id)
    else:
        form = ParcelRequestForm()
    return render(request, 'parcels/create_parcel.html', {'form': form})

@login_required
def parcel_detail(request, parcel_id):
    parcel = get_object_or_404(ParcelRequest, id=parcel_id)
    return render(request, 'parcels/parcel_detail.html', {'parcel': parcel})



@login_required
def accept_parcel(request, parcel_id):
    # Check if user is a rider
    if request.user.role != 'rider':
        from django.contrib import messages
        messages.error(request, "Only riders can accept parcels.")
        return redirect('rider_dashboard')
    
    parcel = get_object_or_404(ParcelRequest, id=parcel_id)
    if parcel.status == 'requested':
        parcel.rider = request.user
        parcel.status = 'accepted'
        parcel.save()
    return redirect('rider_dashboard')

@login_required
def pickup_parcel(request, parcel_id):
    parcel = get_object_or_404(ParcelRequest, id=parcel_id, rider=request.user)
    if parcel.status == 'accepted':
        parcel.status = 'picked_up'
        parcel.save()
    return redirect('rider_dashboard')

@login_required
def deliver_parcel(request, parcel_id):
    parcel = get_object_or_404(ParcelRequest, id=parcel_id, rider=request.user)
    if parcel.status == 'picked_up':
        parcel.status = 'delivered'
        parcel.save()
    return redirect('rider_dashboard')

