# My Django imports
from django.urls import path

# My app imports
from ONB_auth.views import (
    RegisterView,
    LoginView,
    LogoutView,
    DashboardView,
    NotificationView,
)

app_name = 'auth'

urlpatterns = [
    # Authentication and Authorization
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    #Dashboard
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('notifications', NotificationView.as_view(), name='notifications'),
]