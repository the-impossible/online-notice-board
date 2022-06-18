# My Django imports
from django import forms

# My app imports
from ONB_auth.models import Accounts

class AccountCreationForm(forms.ModelForm):
    fullname = forms.CharField(required=True, help_text='Please enter your Fullname',widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'autofocus':'',
        }
    ))

    username = forms.CharField(required=True,help_text='Please enter your registration number', widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Enter your registration number',
        }
    ))

    password = forms.CharField(required=True, help_text='Password must contain at least 6 characters',
    widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Password ',
            'type':'Password',
        }
    ))

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise forms.ValidationError('Password too short, should be at least 6 characters!')

        return password

    def clean_username(self):
        username = self.cleaned_data.get('username')
        num = len(username)
        if num < 12 or num > 12:
            raise forms.ValidationError('Registration number, should be exactly 12 characters!')
        if Accounts.objects.filter(username=username).exists():
            raise forms.ValidationError('Registration number Already exist!')

        return username

    class Meta:
        model = Accounts
        fields = ('fullname', 'username', 'password')