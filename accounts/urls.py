from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('check-username/', views.check_username, name='check-username'),
    path('users/', views.manage_users, name='manage_users'),
    path('my-account/', views.my_account_view, name='my_account'),
]