from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import login

from .forms import UserRegistrationForm, RiderRegisterForm


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'


class RiderLoginView(LoginView):
    template_name = 'accounts/rider_login.html'

    def form_valid(self, form):
        user = form.get_user()

        if user.role != 'rider':
            messages.error(self.request, "Access denied. Riders only.")
            return self.form_invalid(form)

        rider_profile = getattr(user, 'rider_profile', None)
        if not rider_profile:
            messages.error(self.request, "Rider profile not found.")
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('rider_dashboard')


# ✅ Customer registration (AUTO LOGIN)
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome! Account created successfully.")
            return redirect('home')   # customer landing page
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


# ✅ Rider registration (AUTO LOGIN)
def rider_register_view(request):
    if request.method == 'POST':
        form = RiderRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome! You have been registered successfully.")
            return redirect('rider_dashboard')
    else:
        form = RiderRegisterForm()

    return render(request, 'accounts/rider_register.html', {'form': form})
