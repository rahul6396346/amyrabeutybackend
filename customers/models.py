from django.db import models

class Customer(models.Model):
    GENDER_CHOICES = [
        ('FEMALE', 'Female'),
        ('MALE', 'Male'),
        ('OTHER', 'Other'),
    ]
    
    MEMBERSHIP_CHOICES = [
        ('NONE', 'None'),
        ('SILVER', 'Silver'),
        ('GOLD', 'Gold'),
        ('PLATINUM', 'Platinum'),
    ]

    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='FEMALE')
    dob = models.DateField(null=True, blank=True)
    anniversary_date = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    preferred_services = models.TextField(blank=True, null=True) # Could be JSON or comma separated
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_CHOICES, default='NONE')
    profile_image = models.ImageField(upload_to='customers/', null=True, blank=True)
    
    # Aggregates
    total_visits = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False) # Soft delete
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

class Membership(models.Model): # Keeping this if needed for legacy, but user wants it in Customer model too? 
    # Actually user asked for membership_type in Customer model. I'll stick to that but maybe this can store history.
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='customer_membership')
    tier = models.CharField(max_length=50, default='Silver')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    expiry_date = models.DateField()

    def __str__(self):
        return f"{self.customer.full_name} - {self.tier}"
