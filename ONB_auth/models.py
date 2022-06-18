# My Django imports
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# My app imports

# Create your models here.
class AccountsManager(BaseUserManager):
    def create_user(self, username, fullname, password=None):

        #creates a user with the parameters
        if not username:
            raise ValueError('Registration Number is required!')

        if password is None:
            raise ValueError('Password is required!')

        if fullname is None:
            raise ValueError('Fullname is required!')

        user = self.model(
            username = username.upper().strip(),
            fullname=fullname.title().strip(),
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, fullname, password):
        # create a superuser with the above parameters
        if password is None:
            raise ValueError('Password should not be empty')

        if fullname is None:
            raise ValueError('Fullname is required!')

        if not username:
            raise ValueError('Registration number is required!')

        user = self.create_user(
            username=username.upper().strip(),
            fullname=fullname.title().strip(),
            password=password,
        )

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)

        return user

class Accounts(AbstractBaseUser, PermissionsMixin):
    fullname = models.CharField(max_length=30, db_index=True)
    username = models.CharField(max_length=12, db_index=True, unique=True, blank=True)

    date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last_login', auto_now=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['fullname']

    objects = AccountsManager()

    def get_name(self):
        return self.fullname

    def __str__(self):
        return f'{self.username}'

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return True

    class Meta:
        db_table = 'Accounts'
        verbose_name_plural = 'Accounts'