from django.urls import path
from .views import *
from user.views import CustomLoginView


urlpatterns = [
    path('dashboard',dashboard,name='dashboard'),
    path("orderupdate/<pk>",OrderStaffUpdate.as_view(),name='orderstaffupdate'),
    path('tablelist',tables,name='tablelist'),
    path('tablecreate',TableCreateView.as_view(),name='tablecreate'),
    path('createcategory',CategoryCreateView.as_view(),name='createcategory'),
    path('categoriesview/<pk>',CategoryUpdateView.as_view(),name='categoriesview'),
    path('categorylist',CategoryListView.as_view(),name='categorieslist'),
    path('newitem' , ProductCreateView.as_view(),name='newitem'),
    path('updateitem/<pk>' , ProductUpdateView.as_view(),name='updateitem'),
    path('', CustomLoginView.as_view(template_name='user/login.html',), name='login'),
    path('manager/', Managerview.as_view(), name='manager'),

]