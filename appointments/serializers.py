from rest_framework import serializers
from .models import Appointment, AppointmentService
from django.db.models import Q

class AppointmentServiceSerializer(serializers.ModelSerializer):
    service_name = serializers.ReadOnlyField(source='service.name')
    
    class Meta:
        model = AppointmentService
        fields = ['id', 'service', 'service_name', 'price_at_booking']

class AppointmentSerializer(serializers.ModelSerializer):
    customer_name = serializers.ReadOnlyField(source='customer.full_name')
    customer_phone = serializers.ReadOnlyField(source='customer.phone')
    staff_name = serializers.ReadOnlyField(source='assigned_staff.user.get_full_name')
    services_list = AppointmentServiceSerializer(source='appointmentservice_set', many=True, read_only=True)
    service_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    class Meta:
        model = Appointment
        fields = [
            'id', 'customer', 'customer_name', 'customer_phone', 'services_list', 
            'service_ids', 'assigned_staff', 'staff_name', 'appointment_date', 
            'start_time', 'end_time', 'status', 'notes', 'advance_payment', 
            'payment_status', 'booking_source', 'branch', 'created_at'
        ]

    def validate(self, data):
        staff = data.get('assigned_staff')
        date = data.get('appointment_date')
        start = data.get('start_time')
        end = data.get('end_time')
        
        if staff and date and start and end:
            overlapping = Appointment.objects.filter(
                assigned_staff=staff,
                appointment_date=date,
                status__in=['PENDING', 'CONFIRMED', 'IN_PROGRESS']
            ).filter(
                Q(start_time__lt=end, end_time__gt=start)
            )
            
            if self.instance:
                overlapping = overlapping.exclude(id=self.instance.id)
                
            if overlapping.exists():
                raise serializers.ValidationError({
                    "assigned_staff": "This staff member already has an appointment during this time slot."
                })
        
        return data

    def create(self, validated_data):
        from services.models import Service # Late import
        service_ids = validated_data.pop('service_ids', [])
        appointment = Appointment.objects.create(**validated_data)
        
        for s_id in service_ids:
            try:
                service = Service.objects.get(id=s_id)
                AppointmentService.objects.create(
                    appointment=appointment,
                    service=service,
                    price_at_booking=service.price
                )
            except Service.DoesNotExist:
                pass
            
        return appointment

    def update(self, instance, validated_data):
        from services.models import Service # Late import
        service_ids = validated_data.pop('service_ids', None)
        instance = super().update(instance, validated_data)
        
        if service_ids is not None:
            AppointmentService.objects.filter(appointment=instance).delete()
            for s_id in service_ids:
                try:
                    service = Service.objects.get(id=s_id)
                    AppointmentService.objects.create(
                        appointment=instance,
                        service=service,
                        price_at_booking=service.price
                    )
                except Service.DoesNotExist:
                    pass
        
        if instance.status == 'COMPLETED':
            customer = instance.customer
            customer.total_visits += 1
            total_val = sum(s.price_at_booking for s in instance.appointmentservice_set.all())
            customer.total_spent += total_val
            customer.save()

            # Auto-generate Invoice
            from billing.models import Invoice, InvoiceItem
            if not Invoice.objects.filter(appointment=instance).exists():
                invoice = Invoice.objects.create(
                    appointment=instance,
                    customer=instance.customer,
                    sub_total=total_val,
                    tax_percentage=18.0, # Default GST or similar
                    status='PENDING',
                    amount_paid=instance.advance_payment
                )
                
                for app_service in instance.appointmentservice_set.all():
                    InvoiceItem.objects.create(
                        invoice=invoice,
                        item_type='SERVICE',
                        description=app_service.service.name,
                        unit_price=app_service.price_at_booking,
                    )
            
        return instance
