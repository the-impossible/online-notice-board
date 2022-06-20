# My Django imports
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

# My app imports
from ONB_auth.form import AccountCreationForm, AccountEditForm
from ONB_auth.models import Accounts

# Create your views here.
class DashboardView(View):
    def get(self, request):
        return render(request, 'admin/dashboard.html')

class CreateAccountView(View):
    def get(self, request):
        context = {
            'form':AccountCreationForm()
        }
        return render(request, 'admin/create_account.html', context)

    def post(self, request):
        form = AccountCreationForm(request.POST)
        lecturer = request.POST.get('lecturer')
        if form.is_valid():
            form = form.save(commit=False)
            message = 'Student'
            if lecturer:
                form.is_staff = True
                message = 'Lecturer'

            form.set_password(form.password)
            form.save()

            messages.success(request, f'{message} account has been created')
            return redirect('super:create_account')

        messages.error(request, f'Invalid credentials')
        return render(request, 'admin/create_account.html', {'form':form})

class ManageStudentView(View):
    def get(self, request):
        students = Accounts.objects.filter(is_staff=False)
        context = {
            'students':students,
        }

        return render(request, 'admin/manage_student.html', context)

class ManageStaffView(View):
    def get(self, request):
        staffs = Accounts.objects.filter(is_staff=True)
        context = {
            'staffs':staffs,
        }

        return render(request, 'admin/manage_staff.html', context)

class ProfileView(View):
    def get(self, request, user_id):
        try:
            user = Accounts.objects.get(id=user_id)
            form = AccountEditForm(instance=user)
            context = {
                'form':form,
                'acct':user,
            }
        except Accounts.DoesNotExist:
            messages.error(request, 'Account does not exists')
            return redirect('super:dashboard')

        return render(request, 'admin/profile.html', context)

    def post(self, request, user_id):
        try:
            user = Accounts.objects.get(id=user_id)
            form = AccountEditForm(request.POST, instance=user)

            if 'profile' in request.POST:
                if form.is_valid():
                    form = form.save(commit=False)
                    lecturer = request.POST.get('lecturer')
                    if lecturer:
                        form.is_staff = True
                    else:
                        form.is_staff = False
                    form.save()
                    messages.success(request, 'Profile update successful!')
                    return redirect('super:profile', user_id)
                else:
                    messages.error(request, 'Error updating profile!')
                    context = {
                        'form':form,
                    }
            if 'password' in request.POST:
                password = request.POST.get('password1')
                password1 = request.POST.get('password2')

                if (password != password1):
                    messages.error(request, 'Password does not match!')
                    return redirect('super:profile', user_id)

                if(len(password1) < 6):
                    messages.error(request, 'Password too short!')
                    return redirect('super:profile', user_id)

                user = Accounts.objects.get(id=user_id)
                user.set_password(password)
                user.save()

                messages.success(request, 'Password reset successful!!')
                if request.user == user:
                    return redirect('auth:login')

                if request.user.is_superuser:
                    return redirect('super:profile', user_id)
                return redirect('auth:login')

        except Accounts.DoesNotExist:
            messages.error(request, 'Account does not exists')
            return redirect('super:dashboard')

        return render(request, 'admin/profile.html', context)

class ChangeRoleView(View):
    def get(self, request, user_id, role):
        try:
            user = Accounts.objects.get(id=user_id)
            if role == 'admin':
                user.is_superuser = True
            else:
                user.is_superuser = False
            user.save()
            messages.success(request, f'{user.fullname} role has been changed')
        except Accounts.DoesNotExist:
            messages.error(request, f'Error swapping user role')

        return redirect(to="super:manage_staff")
class DeleteAccountView(View):
    def get(self, request, user_id, role):
        try:
            user = Accounts.objects.get(id=user_id)
            user.delete()
            messages.success(request, f'{user.fullname} has been deleted')
        except Accounts.DoesNotExist:
            messages.error(request, f'Error deleting user')

        if role == 'staff':
            if request.user == user:
                return redirect('auth:login')
            return redirect(to="super:manage_staff")
        return redirect(to="super:manage_student")

