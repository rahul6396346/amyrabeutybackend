from rest_framework import serializers
from .models import Invoice, InvoiceItem

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ['id', 'item_type', 'description', 'quantity', 'unit_price', 'total_price']

class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, read_only=True)
    customer_name = serializers.ReadOnlyField(source='customer.full_name')
    customer_phone = serializers.ReadOnlyField(source='customer.phone')
    appointment_id = serializers.ReadOnlyField(source='appointment.id')

    class Meta:
        model = Invoice
        fields = [
            'id', 'invoice_number', 'appointment', 'appointment_id', 'customer', 'customer_name', 
            'customer_phone', 'sub_total', 'tax_percentage', 'tax_amount', 
            'discount_amount', 'total_amount', 'amount_paid', 'status', 
            'payment_method', 'items', 'created_at'
        ]
