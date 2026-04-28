from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from .models import Appointment
from .serializers import AppointmentSerializer
from django_filters.rest_framework import DjangoFilterBackend

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all().order_by('appointment_date', 'start_time')
    serializer_class = AppointmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['appointment_date', 'assigned_staff', 'status', 'payment_status', 'branch']
    search_fields = ['customer__full_name', 'customer__phone', 'notes']
    ordering_fields = ['appointment_date', 'start_time', 'created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Support for date ranges (calendar view)
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(appointment_date__range=[start_date, end_date])
            
        if self.request.query_params.get('all') == 'true':
            self.pagination_class = None
            
        return queryset

    def destroy(self, request, *args, **kwargs):
        # Soft cancel logic
        instance = self.get_object()
        reason = request.data.get('cancellation_reason', 'No reason provided')
        instance.status = 'CANCELLED'
        instance.cancellation_reason = reason
        instance.save()
        return Response({"message": "Appointment cancelled successfully"}, status=status.HTTP_200_OK)
