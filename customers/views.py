from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from .models import Customer, Membership
from .serializers import CustomerSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers

class MembershipSerializer(serializers.ModelSerializer):
    customer_name = serializers.ReadOnlyField(source='customer.full_name')
    class Meta:
        model = Membership
        fields = '__all__'

class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.filter(is_deleted=False).order_by('-created_at')
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['membership_type', 'is_active', 'gender']
    search_fields = ['full_name', 'phone', 'email']
    ordering_fields = ['full_name', 'total_visits', 'total_spent', 'created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Manager and Staff cannot see the list of customers
        if self.request.user.role in ['MANAGER', 'STAFF'] and self.action == 'list':
            return Customer.objects.none()
        
        if self.request.query_params.get('all') == 'true':
            self.pagination_class = None
        return queryset

    def check_permissions(self, request):
        super().check_permissions(request)
        # Manager and Staff can only 'create' 
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            if request.user.role in ['MANAGER', 'STAFF']:
                self.permission_denied(request, message="You only have permission to add customers.")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete() # Trigger soft delete
        return Response(status=status.HTTP_204_NO_CONTENT)
