from django import forms
from .models import Ride

class RideRequestForm(forms.ModelForm):
    pickup_address = forms.CharField(
        label="Pickup Location",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Select pickup from map or type address",
                "autocomplete": "off",
            }
        ),
    )

    dropoff_address = forms.CharField(
        label="Dropoff Location",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Select dropoff from map or type address",
                "autocomplete": "off",
            }
        ),
    )

    class Meta:
        model = Ride
        fields = ["pickup_address", "dropoff_address"]

    def clean(self):
        cleaned_data = super().clean()
        pickup = cleaned_data.get("pickup_address")
        dropoff = cleaned_data.get("dropoff_address")

        if not pickup:
            self.add_error("pickup_address", "Please select a pickup location from the map.")

        if not dropoff:
            self.add_error("dropoff_address", "Please select a dropoff location from the map.")

        return cleaned_data
