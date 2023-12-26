# from django.urls import path ,include
# from . import views
# from django.contrib.auth import views as auth_views
# urlpatterns = [
# #     path('login/', auth_views.LoginView.as_view(), name= 'login'),
#     path('login',views.login,name='login'),
#     path('logout/' , views.logout_view, name= 'logout' ),
#     # change password urls
#     path('password-change/',
#          auth_views.PasswordChangeView.as_view(),
#          name='password_change'),
#     path('password-change/done/',
#           auth_views.PasswordChangeDoneView.as_view(),
#           name='password_change_done'),

# #reset password urls
#     path('password-reset/',
#          auth_views.PasswordResetView.as_view(),
#          name='password_reset'),
#     path('password-reset/done/',
#          auth_views.PasswordResetDoneView.as_view(),
#          name='password_reset_done'),
#     path('password-reset/<uidb64>/<token>/',
#          auth_views.PasswordResetConfirmView.as_view(),
#          name='password_reset_confirm'),
#     path('password-reset/complete/',
#          auth_views.PasswordResetCompleteView.as_view(),
#          name='password_reset_complete'),
#     path('', views.dashboard, name='dashboard'),
#     path('register/', views.register, name='register'),
# ]

from django.urls import path
from .views import SignUpView, VerifyView, CustomLoginView, ResendVerifyView
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('verify/', VerifyView.as_view(), name='verify'),
    path('verify/resend/', ResendVerifyView.as_view(), name='resend'),
    
    path('login/', CustomLoginView.as_view(template_name='account/login.html',), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/logged_out.html',), name='logout'),

    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='account/password_reset_form.html',form_class=CustomPasswordResetForm), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html',), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
