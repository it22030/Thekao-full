from django.shortcuts import render, redirect

def landing_page(request):
    return render(request, 'home.html')

def home_redirect(request):
    # This was the old home view, now we might want to redirect to landing or restaurants depending on context
    # But for now, let's keep the landing page at '/'
    return redirect('landing_page')
