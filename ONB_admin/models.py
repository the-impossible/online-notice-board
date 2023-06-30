# My Django imports
from django.db import models

# My App imports
from ONB_auth.models import Accounts

# Create your models here.
class Notification(models.Model):
    send_to = (
        ('General Public', 'General Public'),
        ('Student', 'Student'),
        ('Staff', 'Staff'),
        ('Staff and Student', 'Staff and Student'),
    )
    created_by = models.ForeignKey(to=Accounts, on_delete=models.CASCADE, blank=True, null=True, related_name="created_by")
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(null=True, upload_to='uploads/')
    file = models.FileField(upload_to='uploads/')
    receiver = models.CharField(max_length=20, choices=send_to, blank=True, null=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    class Meta:
        verbose_name_plural = 'Notifications'
        db_table = 'Notifications'

    def __str__(self):
        return f'CREATED: {self.created_by} | RECEIVED: {self.receiver}'