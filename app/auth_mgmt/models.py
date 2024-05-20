from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,UserManager,PermissionsMixin
from django.utils import timezone
from decouple import config



class UserManager(BaseUserManager):
    """
        This is custom user manager
    """
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is mandatory.")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is mandatory.")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser,PermissionsMixin):
    """this is my custom myUser subclass of Abstractbaseuser"""
    email = models.EmailField(max_length=254, unique=True)
    recovery_code = models.TextField()
    mfa_enabled = models.BooleanField(default = False)
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(auto_now=True)
    # groups = models.ManyToManyField(Group, blank=True)

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.email  
     
    

