# My Django imports
from django import forms

# My app imports
from ONB_auth.models import Accounts
from ONB_admin.models import Notification

class CreateNotificationForm(forms.ModelForm):
    send_to = (
        ('General Public', 'General Public'),
        ('Student', 'Student'),
        ('Staff', 'Staff'),
        ('Staff and Student', 'Staff and Student'),
    )

    title = forms.CharField(max_length=1000, widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Enter the Title of the notification ',
            'type':'text',
        }
    ))

    image = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={
            'class':'form-control',
            'type':'file',
            'accept':'image/png, image/jpeg'
        }
    ))

    file = forms.FileField(required=False, widget=forms.FileInput(
        attrs={
            'class':'form-control',
            'type':'file',
            'accept':'.doc,.docx,application/msword,application/pdf'
        }
    ))

    receiver = forms.ChoiceField(choices=send_to, required=True, widget=forms.Select(
        attrs={
            'class':'form-select',
        }
    ))

    description = forms.CharField(max_length=1000, widget=forms.Textarea(
        attrs={
            'class':'form-control',
            'placeholder':'Enter the description of the notification ',
            'type':'text',
        }
    ))


    class Meta:
        model = Notification
        fields = ('image', 'title', 'file', 'receiver', 'description')
