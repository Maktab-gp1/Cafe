from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.DashboardView.as_view(), name='manger'),
    path('orders',views.OrderList, name='orderlist'),
    path('tables', views.tables , name='table'),
    path('createtable', views.TableCreateView.as_view(),name='crtable'),
    path('foods',views.FoodsListView.as_view(),name = 'foods'),
    path('newfood',views.FoodCreateView.as_view(),name='newfood'),
    path('newcategory',views.CategoryCreateView.as_view(), name='newcategory'),
    path('updatefood/<pk>',views.FoodUpdateView.as_view(), name='updatefood'),
    path('updatecategory/<pk>',views.CategoryUpdateView.as_view(),name='updatecategory'),
    path('updateinfo/<pk>',views.CafeInfoUpdateView.as_view(),name='updateinfo'),
]



