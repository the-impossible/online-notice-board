# My Django imports
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

# My app imports
from ONB_auth.form import AccountCreationForm

# Create your views here.
class RegisterView(View):
    def get(self, request):
        context = {
            'form':AccountCreationForm()
        }
        return render(request, 'auth/register.html', context)

    def post(self, request):
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.set_password(form.password)
            form.save()
            messages.success(request, 'Account Created Successfully you can now login')
        else:
            messages.error(request, 'Invalid Credentials')
            context = {
                'form':form
            }
            return render(request, 'auth/register.html', context)
        return redirect(to="auth:login")

class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')
