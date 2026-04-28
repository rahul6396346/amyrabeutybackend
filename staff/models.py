from django.db import models
from django.conf import settings

class Staff(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='staff_profile')
    specialization = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username
