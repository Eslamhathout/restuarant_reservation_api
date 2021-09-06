from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
    def create_user(self, email, id_number, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('You have to provide an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.id_number=id_number
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password, id_number):
        """Creates and saves a new superuser"""
        user = self.create_user(email, id_number, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports email"""

    class Staff_Roles:
        Employee = 'Employee'
        Admin = 'Admin'

        @classmethod
        def choices(cls):
            return(
                (cls.Employee, _('Employee')),
                (cls.Admin, _('Admin')),
            )

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    id_number = models.PositiveIntegerField(null=False, unique=True, validators=[MinValueValidator(1000), MaxValueValidator(9999)])
    role = models.CharField(max_length=20, null=False, choices=Staff_Roles.choices())

    objects = UserManager()
    USERNAME_FIELD = 'email'
