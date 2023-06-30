# My Django imports
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.db.models import Q

# My app imports
from ONB_auth.form import AccountCreationForm, AccountEditForm
from ONB_admin.form import CreateNotificationForm
from ONB_admin.models import Notification
from ONB_auth.models import Accounts

# Create your views here.
class DashboardView(View):
    def get(self, request):
        students = Accounts.objects.filter(is_staff=False).count()
        staffs = Accounts.objects.filter(is_staff=True).count()
        staff_notification = Notification.objects.filter(receiver='Staff').count()
        staff_student_notification = Notification.objects.filter(receiver='Staff and Student').count()
        context = {
            'students':students,
            'staffs':staffs,
            'staff_student_notification':staff_student_notification,
            'staff_notification':staff_notification
        }
        return render(request, 'admin/dashboard.html', context)

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

class CreateNotificationView(View):
    def get(self, request):
        context = {
            'form':CreateNotificationForm()
        }
        return render(request, 'admin/create_notice.html', context)

    def post(self, request):
        form = CreateNotificationForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            try:
                user = Accounts.objects.get(id=request.user.id)
                form.created_by = user
                form.save()
                messages.success(request, f'Notification has been sent to the {form.receiver}')
                return redirect('super:notify')
            except Accounts.DoesNotExist:
                messages.error(request, 'User does not exist!!')
                return redirect(to="auth:login")

        messages.error(request, f'Error uploading Notification\n {form.errors} ')
        return render(request, 'admin/create_notice.html', {'form': form})

class ManageNotificationView(View):
    def get(self, request):
        notifications = Notification.objects.all()
        context = {
            'notifications':notifications
        }
        return render(request, 'admin/manage_notification.html', context)

class ViewNotificationView(View):
    def get(self, request, notification_id):
        try:
            notifications = Notification.objects.get(id=notification_id)
            context = {
                'notify':notifications
            }
        except Notification.DoesNotExist:
            messages.error(request, "Error Displaying notification")
            if request.user.is_superuser:
                return redirect(to='super:manage_notification')
            else:
                return redirect(to='auth:notifications')
        if request.user.is_superuser:
            return render(request, 'admin/view_notification.html', context)
        else:
            return render(request, 'auth/view_notification.html', context)

class EditNotificationView(View):
    def get(self, request, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id)
            context = {
                'form':CreateNotificationForm(initial={'receiver':notification.receiver}, instance=notification),
                'notify':notification,
            }
            return render(request, 'admin/edit_notice.html', context)
        except Notification.DoesNotExist:
            messages.error(request, 'Notification does not exist!')
            return redirect('super:manage_notification')

    def post(self, request, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id)
            form = CreateNotificationForm(request.POST, request.FILES, initial={'receiver':notification.receiver}, instance=notification)

            if form.is_valid():
                messages.success(request, 'Notification has been updated successfully!!')
                form.save()
                return redirect('super:view_notification', notification_id)

            messages.error(request, 'Updating notification failed!!')
            return redirect('super:edit_notification', notification_id)

        except Notification.DoesNotExist:
            messages.error(request, 'Notification does not exist!')
            return redirect('super:manage_notification')

class DeleteNotificationView(View):
    def get(self, request, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.delete()
            messages.success(request, 'Notification has been deleted successfully!!')
        except Notification.DoesNotExist:
            messages.error(request, 'Failed: Notification does not exist!')
        return redirect('super:manage_notification')

class SearchNotificationView(View):
    def get(self, request):
        context = {}
        qs = request.GET.get('query')
        if qs:
            if request.user.is_superuser:
                notifications = (
                    Notification.objects.filter(title__icontains=qs) |
                    Notification.objects.filter(description__icontains=qs) |
                    Notification.objects.filter(receiver__icontains=qs) |
                    Notification.objects.filter(created_by__fullname__icontains=qs)
                )
            elif request.user.is_staff:
                notifications = (
                    Notification.objects.filter(
                        Q(title__icontains=qs, receiver='Staff and Student') | Q(title__icontains=qs, receiver='General Public') | Q(title__icontains=qs, receiver='Student') |
                        Q(description__icontains=qs, receiver='Staff and Student') | Q(description__icontains=qs, receiver='General Public') | Q(description__icontains=qs, receiver='Student') |
                        Q(created_by__fullname__icontains=qs, receiver='Staff and Student') | Q(created_by__fullname__icontains=qs, receiver='General Public') | Q(created_by__fullname__icontains=qs, receiver='Student') |
                        Q(receiver__icontains=qs, receiver='Staff and Student') | Q(receiver__icontains=qs, receiver='General Public') | Q(receiver__icontains=qs, receiver='Student')
                    )
                )
            else:
                notifications = (
                    Notification.objects.filter(
                        Q(title__icontains=qs, receiver='Student') | Q(title__icontains=qs, receiver='General Public')|
                        Q(description__icontains=qs, receiver='Student') | Q(description__icontains=qs, receiver='General Public') |
                        Q(created_by__fullname__icontains=qs, receiver='Student') | Q(created_by__fullname__icontains=qs, receiver='General Public') |
                        Q(receiver__icontains=qs, receiver='Student') | Q(receiver__icontains=qs, receiver='General Public')
                    )
                )
            if not notifications:
                messages.error(request, 'No result found')
            context['notifications'] = notifications
            context['qs'] = qs
        else:
            messages.error(request, 'Please input a value advisably use keywords')
            context['qs'] = ''

        return render(request, 'basics/search.html', context)
