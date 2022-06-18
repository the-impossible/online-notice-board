from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# My App imports
from ONB_auth.models import Accounts

# Register your models here.
class AccountsAdmin(UserAdmin):
    list_display = ('username', 'fullname', 'date_joined', 'last_login', 'is_active', 'is_staff', 'is_superuser' )
    search_fields = ('username', 'fullname',)
    ordering = ('username',)
    readonly_fields = ('date_joined', 'last_login',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


# Register your models here.
admin.site.register(Accounts, AccountsAdmin)