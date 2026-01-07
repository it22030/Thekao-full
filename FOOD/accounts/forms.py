from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=User._meta.get_field('role').choices,
        initial='customer',
        widget=forms.HiddenInput()
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)


class RiderRegisterForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=True)
    vehicle_type = forms.CharField(max_length=50, required=True)
    rider_type = forms.ChoiceField(
        choices=[
            ('food', 'Food Delivery'),
            ('parcel', 'Parcel Delivery'),
            ('ride', 'Ride Sharing'),
            ('both', 'Food & Parcel Delivery')
        ],
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'rider'

        if commit:
            user.save()

            from .models import RiderProfile
            profile, created = RiderProfile.objects.get_or_create(user=user)

            profile.phone_number = self.cleaned_data['phone_number']
            profile.vehicle_type = self.cleaned_data['vehicle_type']

            # Reset flags (important!)
            profile.is_food_rider = False
            profile.is_parcel_rider = False
            profile.is_ride_rider = False

            rtype = self.cleaned_data['rider_type']
            if rtype == 'food':
                profile.is_food_rider = True
            elif rtype == 'parcel':
                profile.is_parcel_rider = True
            elif rtype == 'ride':
                profile.is_ride_rider = True
            elif rtype == 'both':
                profile.is_food_rider = True
                profile.is_parcel_rider = True

            profile.save()

        return user
