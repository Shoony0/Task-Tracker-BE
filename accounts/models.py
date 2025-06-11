from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    ADMIN = "admin"
    TASK_CREATOR = "task_creator"
    READ_ONLY = "read_only"
    
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name  

class User(AbstractUser):
    email = models.EmailField(unique=True)  # Ensure email is unique
    roles = models.ManyToManyField(Role, related_name='users')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Remove 'username' from required fields

    def __str__(self):
        return self.email
