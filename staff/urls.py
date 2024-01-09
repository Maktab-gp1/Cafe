from django.urls import path
from .views import *
from user.views import CustomLoginView


urlpatterns = [
    path('dashboard', StaffPanel.as_view(), name='dashboard'),
    path('dashboard', StaffPanel.as_view(), name='dashboard'),
    # path('statusupdate/',StatusUpdateView.as_view(),name='statusupdate'),
    path("orderupdate/<pk>", OrderStaffUpdate.as_view(), name='orderstaffupdate'),
    path('createcategory', CategoryCreateView.as_view(), name='createcategory'),
    path('categoriesview/<pk>', CategoryUpdateView.as_view(), name='categoriesview'),
    path('categorylist', CategoryListView.as_view(), name='categorieslist'),
    path('newitem', ProductCreateView.as_view(), name='newitem'),
    path('updateitem/<pk>', ProductUpdateView.as_view(), name='updateitem'),
    path('', CustomLoginView.as_view(
        template_name='user/login.html',), name='login'),
    path('manager/', Managerview.as_view(), name='manager'),

]
