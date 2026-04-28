from django.db import models
import uuid

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('PARTIAL', 'Partial'),
        ('CANCELLED', 'Cancelled'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('CASH', 'Cash'),
        ('CARD', 'Card'),
        ('UPI', 'UPI/GPay'),
        ('WALLET', 'Salon Wallet'),
    ]

    invoice_number = models.CharField(max_length=50, unique=True, editable=False)
    appointment = models.OneToOneField('appointments.Appointment', on_delete=models.SET_NULL, null=True, blank=True, related_name='invoice')
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, related_name='invoices')
    
    sub_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0) # e.g. 18%
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='CASH')
    
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            # Generate unique invoice number: INV-24-XXXX
            from django.utils import timezone
            year = timezone.now().strftime('%y')
            last_invoice = Invoice.objects.filter(invoice_number__contains=f'INV-{year}').order_by('-id').first()
            if last_invoice:
                last_num = int(last_invoice.invoice_number.split('-')[-1])
                new_num = str(last_num + 1).zfill(5)
            else:
                new_num = '00001'
            self.invoice_number = f'INV-{year}-{new_num}'
        
        # Calculate total if not set
        self.tax_amount = (self.sub_total * self.tax_percentage) / 100
        self.total_amount = self.sub_total + self.tax_amount - self.discount_amount
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.invoice_number

class InvoiceItem(models.Model):
    ITEM_TYPE_CHOICES = [
        ('SERVICE', 'Service'),
        ('PRODUCT', 'Product'),
        ('OTHER', 'Other'),
    ]

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES, default='SERVICE')
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.description} ({self.invoice.invoice_number})"
