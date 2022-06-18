# Django Imports
from django.urls import path

# My app imports
from ONB_basics.views import (
    HomeView,
)

app_name = 'basics'

urlpatterns = [
    # Static pages
    path('', HomeView.as_view(), name='home'),
]