from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """

    def create_user(self, username, password, user_role, **extra_fields):
        if not username:
            raise ValueError(_('Users must have a username.'))
        if not user_role:
            raise ValueError(_('Users must have a user_role.'))
        user = self.model(username=username, user_role=user_role, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, user_role, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, password, user_role, **extra_fields)


class User(AbstractUser):
    class UserRoleEnums(models.TextChoices):
        DOCTOR = "DOCTOR", _("Doctor")
        PATIENT = "PATIENT", _("Patient")

    user_role = models.CharField(choices=UserRoleEnums.choices, default=UserRoleEnums.PATIENT, max_length=20)

    REQUIRED_FIELDS = ["email", "user_role"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.user_role} {self.get_full_name()}"
