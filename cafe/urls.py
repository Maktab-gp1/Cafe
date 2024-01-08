from django.urls import path, include
from cafe import views

urlpatterns = [
    path('home', views.home, name='main'),
    path('', views.home, name='main'),
    path('menu', views.menu, name='menu'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('confirm/',views.Confirm.as_view(),name='confirm'),
    path('about', views.about, name='about'),
    path('service', views.service, name='service'),
    path('testi', views.testimonial, name='testimonial'),
    # path('staff', views.StaffPanel.as_view(), name='staff'),
    # path('booking', views.booking.as_view(), name='booking'),
   


]
