from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from customers.views import CustomerViewSet, MembershipViewSet
from services.views import ServiceViewSet, ServiceCategoryViewSet
from appointments.views import AppointmentViewSet
from billing.views import InvoiceViewSet
from .dash_views import DashboardStatsView

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'memberships', MembershipViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'service-categories', ServiceCategoryViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'invoices', InvoiceViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/admin/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('api/', include(router.urls)),
]
