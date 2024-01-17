from django.urls import path
from . import views
app_name = 'shop'
urlpatterns = [
        path('list/<slug:category>'
          , views.ProductListView.as_view(),
          name='productlist'),    
        path('detail/<slug:slug>',
          views.ProductDetailView.as_view(),
          name='productdetail'),
        path('',views.ProductListView.as_view() ,name='homeview'),
         ]
