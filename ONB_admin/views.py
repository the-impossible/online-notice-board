# My Django imports
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

# My app imports
from ONB_auth.form import AccountCreationForm
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