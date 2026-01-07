from django.db import models
from django.conf import settings
from decimal import Decimal

User = settings.AUTH_USER_MODEL


class Ride(models.Model):
    STATUS_REQUESTED = "requested"
    STATUS_ACCEPTED = "accepted"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_COMPLETED = "completed"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_REQUESTED, "Requested"),
        (STATUS_ACCEPTED, "Accepted"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    # Relations
    passenger = models.ForeignKey(
        User,
        related_name="rides_as_passenger",
        on_delete=models.CASCADE
    )
    driver = models.ForeignKey(
        User,
        related_name="rides_as_driver",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    # Addresses
    pickup_address = models.CharField(max_length=255)
    dropoff_address = models.CharField(max_length=255)

    # Coordinates
    pickup_lat = models.FloatField(null=True, blank=True)
    pickup_lng = models.FloatField(null=True, blank=True)
    dropoff_lat = models.FloatField(null=True, blank=True)
    dropoff_lng = models.FloatField(null=True, blank=True)

    # Ride Data
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_REQUESTED
    )

    fare = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    distance_km = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    # Feedback
    rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="1 to 5 rating"
    )
    feedback = models.TextField(blank=True)

    # Financials
    rider_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )
    platform_profit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )

    class Meta:
        ordering = ["-created_at"]

    def calculate_commission(self):
        """
        Calculates driver payout and platform profit
        """
        try:
            from core.models import GlobalSettings
            settings = GlobalSettings.load()
            commission_percent = Decimal(settings.ride_commission_percentage)
        except Exception:
            commission_percent = Decimal("80")  # fallback

        driver_cut = (self.fare * commission_percent) / Decimal("100")
        platform_cut = self.fare - driver_cut

        return driver_cut, platform_cut

    def save(self, *args, **kwargs):
        # Calculate commission only once when fare exists
        if self.fare and self.rider_fee == Decimal("0.00"):
            self.rider_fee, self.platform_profit = self.calculate_commission()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ride #{self.id} ({self.get_status_display()})"


class DriverLocation(models.Model):
    driver = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="current_location"
    )
    lat = models.FloatField()
    lng = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Driver Location"
        verbose_name_plural = "Driver Locations"

    def __str__(self):
        return f"{self.driver} @ ({self.lat}, {self.lng})"
class SharedRide(models.Model):
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    total_seats = models.PositiveIntegerField(default=4)
    available_seats = models.PositiveIntegerField(default=4)
    fare_per_seat = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pickup_location} → {self.dropoff_location}"
