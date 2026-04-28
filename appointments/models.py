from django.db import models
from django.conf import settings

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('NO_SHOW', 'No Show'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PARTIAL', 'Partial'),
        ('PAID', 'Paid'),
    ]

    SOURCE_CHOICES = [
        ('WALK_IN', 'Walk-in'),
        ('ONLINE', 'Online'),
        ('CALL', 'Call'),
        ('WHATSAPP', 'WhatsApp'),
    ]

    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, related_name='appointments')
    services = models.ManyToManyField('services.Service', through='AppointmentService')
    assigned_staff = models.ForeignKey('staff.Staff', on_delete=models.SET_NULL, null=True, related_name='appointments')
    
    appointment_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    notes = models.TextField(blank=True, null=True)
    
    advance_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    
    booking_source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='WALK_IN')
    branch = models.CharField(max_length=100, default='Main Branch')
    
    cancellation_reason = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['appointment_date', 'start_time']

    def __str__(self):
        return f"{self.customer.full_name if hasattr(self.customer, 'full_name') else 'Customer'} - {self.appointment_date} ({self.start_time})"

class AppointmentService(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    service = models.ForeignKey('services.Service', on_delete=models.CASCADE)
    price_at_booking = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.appointment} - {self.service}"
