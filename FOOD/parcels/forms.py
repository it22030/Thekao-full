from django import forms
from .models import ParcelRequest

class ParcelRequestForm(forms.ModelForm):
    class Meta:
        model = ParcelRequest
        fields = ['pickup_address', 'dropoff_address', 'receiver_name', 'receiver_phone', 'weight_kg', 'description']
        widgets = {
            'pickup_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pickup Address'}),
            'dropoff_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dropoff Address'}),
            'receiver_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Receiver Name'}),
            'receiver_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Receiver Phone'}),
            'weight_kg': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Weight (kg)'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'What is in the package?'}),
        }
