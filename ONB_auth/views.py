# My Django imports
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

# My app imports
from ONB_auth.form import AccountCreationForm
from ONB_admin.models import Notification
from ONB_auth.models import Accounts

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
                        return redirect('auth:dashboard')

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

class DashboardView(View):
    def get(self, request):
        staff_notification = Notification.objects.filter(
            Q(receiver='Staff and Student') | Q(receiver='Staff') | Q(receiver='General Public')
        ).count()

        student_notification = Notification.objects.filter(
            Q(receiver='Staff and Student') | Q(receiver='Student') | Q(receiver='General Public')
        ).count()

        context = {
            'student_notification':student_notification,
            'staff_notification':staff_notification
        }
        return render(request, 'auth/dashboard.html', context)

class NotificationView(View):
    def get(self, request):
        context = {}
        if not request.user.is_staff:
            notifications = (
                Notification.objects.filter(
                    Q(receiver='Student') |
                    Q(receiver='General Public')|
                    Q(receiver='Staff and Student')
                )
            )
            context['notifications'] = notifications
        else:
            notifications = (
                Notification.objects.filter(
                    Q(receiver='Staff') |
                    Q(receiver='Student') |
                    Q(receiver='General Public')|
                    Q(receiver='Staff and Student')
                )
            )
            context['notifications'] = notifications
        return render(request, 'auth/notifications.html', context)
