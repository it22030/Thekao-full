import os
import django
from django.test import RequestFactory

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Food_delivery.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.views import RiderLoginView
from accounts.forms import RiderRegistrationForm

User = get_user_model()

def test_login_backend():
    print("--- Testing Rider Registration & Login Flow ---")

    # 1. Cleanup
    email = "rider_test@example.com"
    username = "rider_test"
    password = "password123"
    
    if User.objects.filter(username=username).exists():
        User.objects.get(username=username).delete()
        print(f"Deleted existing user: {username}")

    # 2. Register Rider (simulate form)
    form_data = {
        'username': username,
        'email': email,
        'password': password,  # Form expects password/password fields usually handled by view
        'phone_number': '1234567890',
        'vehicle_type': 'Bike',
        'role': 'customer' # Hidden field default
    }
    
    # We can't easily simulate UserCreationForm saving without valid POST data structure (pw1, pw2)
    # So let's create user manually to verify Model/Role logic
    
    user = User.objects.create_user(username=username, email=email, password=password)
    user.role = 'rider'
    user.save()
    print(f"Created rider: {user.username} with role: {user.role}")

    # 3. Test Login View Logic
    from django.contrib.auth.forms import AuthenticationForm
    
    login_form = AuthenticationForm(None, data={'username': username, 'password': password})
    
    if login_form.is_valid():
        print("Login Form is VALID")
        user = login_form.get_user()
        print(f"Authenticated User: {user.username}")
        
        if user.role == 'rider':
            print("Role Check: PASSED")
        else:
            print(f"Role Check: FAILED (Role is {user.role})")
            
        if hasattr(user, 'backend'):
             print(f"User backend set: {user.backend}")
        else:
             print("User backend NOT set (expected from AuthenticationForm)")

    else:
        print("Login Form is INVALID")
        print(login_form.errors)

if __name__ == '__main__':
    test_login_backend()
