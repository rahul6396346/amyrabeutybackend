from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'id', 'full_name', 'phone', 'email', 'gender', 'dob', 
            'anniversary_date', 'address', 'notes', 'preferred_services', 
            'membership_type', 'profile_image', 'total_visits', 'total_spent',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total_visits', 'total_spent', 'created_at', 'updated_at']

    def to_representation(self, instance):
        output = super().to_representation(instance)
        request = self.context.get('request')
        if request and hasattr(request.user, 'role') and request.user.role == 'STAFF':
            output['phone'] = '********' + (output['phone'][-2:] if output['phone'] else '')
        return output

    def validate_phone(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Phone number must be at least 10 digits.")
        return value
