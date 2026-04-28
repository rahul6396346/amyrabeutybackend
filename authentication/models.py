from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    OWNER = 'OWNER'
    MANAGER = 'MANAGER'
    STAFF = 'STAFF'
    
    ROLE_CHOICES = [
        (OWNER, 'Owner'),
        (MANAGER, 'Manager'),
        (STAFF, 'Staff'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=STAFF)
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return f"{self.username} ({self.role})"
