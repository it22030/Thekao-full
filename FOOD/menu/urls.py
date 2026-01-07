from django.urls import path
from . import views

urlpatterns = [
    path('restaurant/<int:restaurant_id>/', views.menu_detail, name='menu_detail'),
]
