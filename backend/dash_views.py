from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count
from appointments.models import Appointment
from billing.models import Invoice
from customers.models import Customer
from django.utils import timezone
from datetime import timedelta

class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()
        
        # Revenue stats
        total_revenue = Invoice.objects.filter(status='PAID').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        
        # Customer stats
        total_customers = Customer.objects.count()
        
        # Appointment stats
        upcoming_appointments = Appointment.objects.filter(
            appointment_date__gte=today,
            status__in=['PENDING', 'CONFIRMED']
        ).count()
        
        # Recent activity
        recent_appointments = Appointment.objects.all().order_by('-created_at')[:5]
        recent_data = []
        for app in recent_appointments:
            recent_data.append({
                'id': app.id,
                'customer_name': app.customer.full_name,
                'service': app.appointmentservice_set.first().service.name if app.appointmentservice_set.exists() else 'Consultation',
                'time': app.start_time.strftime('%I:%M %p'),
                'status': app.status
            })

        return Response({
            'total_revenue': total_revenue,
            'total_customers': total_customers,
            'upcoming_appointments': upcoming_appointments,
            'services_done': Appointment.objects.filter(status='COMPLETED').count(),
            'recent_appointments': recent_data
        })
