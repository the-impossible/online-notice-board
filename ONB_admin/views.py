# My Django imports
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

# My app imports
from ONB_auth.form import AccountCreationForm

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
        return render(request, 'admin/create_account.html', {'form':form})