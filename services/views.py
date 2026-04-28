from rest_framework import viewsets, filters
from .models import Service, ServiceCategory
from .serializers import ServiceSerializer, ServiceCategorySerializer

class ServiceCategoryViewSet(viewsets.ModelViewSet):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('all') == 'true':
            self.pagination_class = None
        return queryset

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        if self.request.query_params.get('all') == 'true':
            self.pagination_class = None
        return queryset
