#Django Imports
from django.shortcuts import render
from django.views import View

#My App imports
from ONB_admin.models import Notification

# Create your views here.
class HomeView(View):
    def get(self, request):
        notifications = Notification.objects.all()
        context = {
            'notifications':notifications
        }
        return render(request,'basics/index.html', context)