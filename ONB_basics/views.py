#Django Imports
from django.shortcuts import render
from django.views import View

#My App imports
from ONB_admin.models import Notification

# Create your views here.
class HomeView(View):
    def get(self, request):
        notifications = Notification.objects.filter(receiver='General Public')
        context = {
            'notifications':notifications
        }
        return render(request,'basics/index.html', context)

class ViewNotificationView(View):
    def get(self, request, notification_id):
        try:
            notifications = Notification.objects.get(id=notification_id)
            context = {
                'notify':notifications
            }
        except Notification.DoesNotExist:
            messages.error(request, "Error Displaying notification")
            return redirect(to='basics:home')
        return render(request, 'basics/detail.html', context)