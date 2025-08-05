from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError

def non_empty_string(value):
    if not value.strip():
        raise ValidationError("This field cannot be empty.")

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    firebase_uid = models.CharField(max_length=255, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, validators=[non_empty_string])
    last_name = models.CharField(max_length=30, validators=[non_empty_string])
    phone_number = models.CharField(max_length=15, validators=[non_empty_string])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    def __str__(self):
        return self.email
    

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['email']
