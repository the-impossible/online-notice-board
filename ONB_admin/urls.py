# My Django imports
from django.urls import path

# My app imports
from ONB_admin.views import (
    DashboardView,
    CreateAccountView,
    ManageStudentView,
    ManageStaffView,
    ProfileView,
    ChangeRoleView,
    DeleteAccountView,
    CreateNotificationView,
    ManageNotificationView,
    ViewNotificationView,
    EditNotificationView,
    DeleteNotificationView,
)

app_name = 'admin'

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    # Accounts
    path('create_account', CreateAccountView.as_view(), name='create_account'),
    path('manage_student', ManageStudentView.as_view(), name='manage_student'),
    path('manage_staff', ManageStaffView.as_view(), name='manage_staff'),
    # Profile
    path('profile/<int:user_id>/', ProfileView.as_view(), name='profile'),
    # Change role
    path('role/<int:user_id>/<str:role>/', ChangeRoleView.as_view(), name='role'),
    # Delete Account
    path('delete/<int:user_id>/<str:role>/', DeleteAccountView.as_view(), name='delete'),
    # Notification
    path('notify', CreateNotificationView.as_view(), name='notify'),
    path('manage_notification', ManageNotificationView.as_view(), name='manage_notification'),
    path('view_notification/<int:notification_id>', ViewNotificationView.as_view(), name='view_notification'),
    path('edit_notification/<int:notification_id>', EditNotificationView.as_view(), name='edit_notification'),
    path('delete_notification/<int:notification_id>', DeleteNotificationView.as_view(), name='delete_notification'),

]