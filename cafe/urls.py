from django.urls import path
from .views import *

urlpatterns = [
    path('home', home, name='main'),
    path('menu', menu, name='menu'),
    path('cart', cart, name='cart'),
    path('checkout', checkout, name='checkout'),
    path('staff', staff, name='staff'),
    path('about', about, name='about'),

]
