from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Normal kullanıcı oluşturma fonksiyonu.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, is_active=True, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Süper kullanıcı oluşturma fonksiyonu.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, help_text="User email address")
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    is_staff = models.BooleanField(default=False, help_text="Designates whether the user can log into this admin site.")
    is_active = models.BooleanField(default=True, help_text="Designates whether this user should be treated as active.")
    date_joined = models.DateTimeField(default=timezone.now)

    # Ek alanlar ekleyebilirsiniz örneğin phone_number, profile_image, vs.

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email dışında gerekli alanlar ekleyebilirsiniz

    def __str__(self):
        return self.email
