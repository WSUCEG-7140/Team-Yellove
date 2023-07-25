from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# ISSUE: Design the data models and relationships #12

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a new CustomUser with the given email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a new CustomUser with superuser privileges.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    """
    Custom user model representing a user in the system.
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # The field that will be used as the unique identifier for authentication
    USERNAME_FIELD = 'email'
    
    # Fields required when creating a user using the createsuperuser management command
    REQUIRED_FIELDS = ['first_name', 'last_name']

    # Manager for the CustomUser model
    objects = CustomUserManager()

    def __str__(self):
        return self.email
