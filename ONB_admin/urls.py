# My Django imports
from django.urls import path

# My app imports
from ONB_admin.views import (
    DashboardView,
    CreateAccountView,
)

app_name = 'admin'

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('create_account', CreateAccountView.as_view(), name='create_account'),
]