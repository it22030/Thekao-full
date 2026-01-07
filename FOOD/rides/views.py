from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.utils import timezone
from math import radians, cos, sin, asin, sqrt
from decimal import Decimal

from .models import Ride
from .forms import RideRequestForm


# -----------------------------
# Utility: Distance Calculation
# -----------------------------
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate distance between two lat/lng points in KM
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return 6371 * c  # Earth radius in KM


# -----------------------------
# Passenger Home
# -----------------------------
@login_required
def ride_home(request):
    active_ride = Ride.objects.filter(
        passenger=request.user,
        status__in=["requested", "accepted", "in_progress"]
    ).last()

    recent_rides = Ride.objects.filter(
        passenger=request.user,
        status="completed"
    ).order_by("-created_at")[:5]

    form = RideRequestForm()

    return render(request, "rides/home.html", {
        "active_ride": active_ride,
        "recent_rides": recent_rides,
        "form": form,
    })


# -----------------------------
# Create Ride
# -----------------------------
@login_required
def create_ride(request):
    if request.method != "POST":
        return redirect("rides:ride_home")

    form = RideRequestForm(request.POST)
    if not form.is_valid():
        return render(request, "rides/home.html", {"form": form})

    ride = form.save(commit=False)
    ride.passenger = request.user
    ride.status = "requested"

    # Coordinates from map
    try:
        ride.pickup_lat = float(request.POST.get("pickup_lat"))
        ride.pickup_lng = float(request.POST.get("pickup_lng"))
        ride.dropoff_lat = float(request.POST.get("dropoff_lat"))
        ride.dropoff_lng = float(request.POST.get("dropoff_lng"))
    except (TypeError, ValueError):
        form.add_error(None, "Please select pickup and dropoff from the map.")
        return render(request, "rides/home.html", {"form": form})

    # Distance & Fare
    ride.distance_km = Decimal(haversine(
        ride.pickup_lng,
        ride.pickup_lat,
        ride.dropoff_lng,
        ride.dropoff_lat,
    ))

    BASE_FARE = Decimal(50)
    PER_KM_RATE = Decimal(20)
    ride.fare = BASE_FARE + (ride.distance_km * PER_KM_RATE)

    ride.save()
    return redirect("rides:ride_detail", ride_id=ride.id)


# -----------------------------
# Ride Detail / Tracking Page
# -----------------------------
@login_required
def ride_detail(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id)

    # Only passenger or assigned driver can view
    if request.user not in [ride.passenger, ride.driver]:
        return HttpResponseForbidden("You are not allowed to view this ride.")

    return render(request, "rides/ride_detail.html", {"ride": ride})


# -----------------------------
# Driver Dashboard
# -----------------------------



# -----------------------------
# Accept Ride
# -----------------------------
@login_required
def accept_ride(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id)

    if ride.status != "requested":
        return redirect("rider_dashboard")

    ride.driver = request.user
    ride.status = "accepted"
    ride.save()

    return redirect("rider_dashboard")


# -----------------------------
# Start Ride
# -----------------------------
@login_required
def start_ride(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id, driver=request.user)

    if ride.status == "accepted":
        ride.status = "in_progress"
        ride.started_at = timezone.now()
        ride.save()

    return redirect("rider_dashboard")


# -----------------------------
# Complete Ride
# -----------------------------
@login_required
def complete_ride(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id, driver=request.user)

    if ride.status == "in_progress":
        ride.status = "completed"
        ride.completed_at = timezone.now()

        if not ride.fare:
            ride.fare = 50 + (ride.distance_km * 20)

        ride.save()

    return redirect("rider_dashboard")


# -----------------------------
# Live Ride Updates API
# -----------------------------
@login_required
def get_ride_updates(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id)

    data = {
        "status": ride.get_status_display(),
        "driver_name": ride.driver.get_full_name() if ride.driver else None,
        "driver_lat": None,
        "driver_lng": None,
    }

    # Optional: if you store live driver location
    if ride.driver:
        try:
            loc = ride.driver.current_location
            data["driver_lat"] = loc.lat
            data["driver_lng"] = loc.lng
        except:
            # If location not set, ignore (or pass default if needed)
            pass

    return JsonResponse(data)
from .models import SharedRide

def shared_rides(request):
    rides = SharedRide.objects.all()
    return render(request, "rides/shared_rides.html", {
        "shared_rides": rides
    })

