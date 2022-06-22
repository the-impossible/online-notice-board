# My Django imports
from django.contrib import admin

# My App imports
from ONB_admin.models import Notification

# Register your models here.
class NotificationAdmin(admin.ModelAdmin):
    model = Notification
    list_display = ('title', 'created_by', 'receiver', 'description', 'date_created')
    search_fields = ('created_by', 'receiver','date_created')
    list_filter = ('date_created',)


# Register your models here.
admin.site.register(Notification, NotificationAdmin)