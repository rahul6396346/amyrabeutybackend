from rest_framework import serializers
from .models import Service, ServiceCategory

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    
    class Meta:
        model = Service
        fields = ('id', 'category', 'category_name', 'name', 'description', 'price', 'duration_minutes', 'is_active')
