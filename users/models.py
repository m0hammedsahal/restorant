from django.db import models
from django.contrib.auth.models import AbstractUser

from users.manager import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, max_length=256, error_messages={'unique': 'Email already exists'})
    is_customer = models.BooleanField(default=False)
    is_store = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    objects = UserManager()

    class Meta:
        db_table = 'users_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-id']
    
    def __str__(self):
        return self.email
    
    