from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(self, email, user_name, phone_no, password):
        if not email:
            raise ValueError('Users must have an email address.')
        if not user_name:
            raise ValueError('Users must have an username.')
        if not phone_no:
            raise ValueError('Users must provide a phone number.')
        if not password:
            raise ValueError('Must provide a valid password.')

        user = self.model(
            email=self.normalize_email(email),
            user_name=user_name,
            phone_no=phone_no,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_name, phone_no, password):

        user = self.create_user(
            email=email, user_name=user_name, phone_no=phone_no, password=password
        )
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(help_text='Your Email Address', unique=True)
    user_name = models.CharField(max_length=30, unique=True)
    phone_no = models.CharField(max_length=10)
    tower_no = models.CharField(max_length=2, blank=True)
    flat_no = models.CharField(max_length=5, blank=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'phone_no']

    def __str__(self):
        return self.user_name

    @property
    def is_staff(self):
        return self.is_superuser


class CustomSession(models.Model):
    session_key = models.CharField(max_length=40)
    otp_field = models.CharField(max_length=6)
    created_time = models.DateTimeField(auto_now_add=True)
