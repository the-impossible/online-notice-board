# My Django imports
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin

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

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            # Authenticate user
            user = authenticate(request, username=username.upper().strip(), password=password)

            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'You are now signed in {user.get_name()}')
                    if user.is_superuser:
                        return redirect('super:dashboard')
                    else:
                        return redirect('basics:dashboard')

                else:
                    messages.warning(request, 'Account not active contact the administrator')
                    return redirect('auth:login')
            else:
                messages.warning(request, 'Invalid login credentials')
                return redirect('auth:login')
        else:
            messages.error(request, 'All fields are required!!')
            return redirect('auth:login')

class LogoutView(View, LoginRequiredMixin):
    def post(self, request):
        logout(request)
        messages.success(request, 'You are now signed out!')
        return redirect('auth:login')