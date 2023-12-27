from django.urls import path
from .views import *

urlpatterns = [
    path('home', home, name='main'),
    path('', home, name='main'),
    path('menu', menu, name='menu'),
    path('cart', cart, name='cart'),
    path('checkout', checkout, name='checkout'),
    path('staff', StaffPanel.as_view(), name='staff'),
    path('confirm/',Confirm.as_view(),name='confirm'),
    path('about', about, name='about'),
    path('service', service, name='service'),
    path('testi', testimonial, name='testimonial'),
    path('booking', booking.as_view(), name='booking'),

]
