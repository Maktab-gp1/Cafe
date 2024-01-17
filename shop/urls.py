from django.urls import path
from . import views
app_name = 'shop'
urlpatterns = [
        path('list/<slug:category>'
            ,views.ProductListView.as_view(),
            name='productlist'),    
        path('',views.HomeView.as_view() ,name='homeview'),
        path("contact", views.Contact.as_view() , name = 'contact'),
        path("about", views.About.as_view() , name = 'about'),
        path("service", views.Service.as_view() , name = 'service')
        ]
