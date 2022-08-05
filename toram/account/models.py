from django.db import models
import uuid
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def _create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('名前を入力してください')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(password, **extra_fields)

    def create_superuser(self, username, password, email=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('is_staff=Trueである必要があります。')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser=Trueである必要があります。')
        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username=models.CharField(verbose_name='username', max_length=30, unique=True,)
    # icon = models.ImageField(verbose_name='プロフィール画像', upload_to="icon/", blank=True, null=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(_("email_address"), unique=True, null=True, blank=True)

    objects = UserManager()
    USERNAME_FIELD="username"


    def __str__(self):
        return self.username

    def clean(self):
        super().clean()