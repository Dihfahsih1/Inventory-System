from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetCompleteView


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('view_profile/', views.view_profile, name='view_profile'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    
    path('login_success/', views.login_success, name='login_success'),

    path('change_password', views.change_password, name='change_password'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='accounts/reset_password.html'), name='reset_password'),

    path('reset_password_done/', auth_views.PasswordResetDoneView.as_view(), {'template_name':'accounts/reset_password_done.html'}, name='reset_password_done'),
    path('reset_password_confirm/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='reset_password_confirm'),
    path('reset_password_complete/', PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='reset_password_complete'),


]