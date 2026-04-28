from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from .models import Invoice
from .serializers import InvoiceSerializer
from django_filters.rest_framework import DjangoFilterBackend

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all().order_by('-created_at')
    serializer_class = InvoiceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_method', 'customer', 'appointment']
    search_fields = ['invoice_number', 'customer__full_name', 'customer__phone']
    ordering_fields = ['created_at', 'total_amount']

    def perform_create(self, serializer):
        # Additional logic if creating invoice manually
        serializer.save()

    def update(self, request, *args, **kwargs):
        # When payment status changes to PAID, we might want to trigger other things
        return super().update(request, *args, **kwargs)
