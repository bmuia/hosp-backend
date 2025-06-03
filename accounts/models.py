# accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Custom User Manager (no changes needed here for this specific issue)
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('roles', 'admin') 

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

# Hospital Model (no changes needed)
class Hospital(models.Model):
    name = models.CharField(max_length=100,unique=True)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Custom User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin')
    )

    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True)
    roles = models.CharField(max_length=50, choices=ROLE_CHOICES)

    # Add these fields for full name
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.email 

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name if self.first_name else self.email