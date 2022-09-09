from django.urls import path
from . import views

urlpatterns = [
    path('',views.mint, name = 'mint'),
    path('register',views.register, name='register'),
] 