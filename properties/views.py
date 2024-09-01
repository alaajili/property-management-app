from rest_framework.viewsets import ModelViewSet
from .models import Property, Tenant, Payment
from .serializers import PropertySerializer, TenantSerializer, PaymentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers, filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PropertyFilter
from .utils import send_payment_notification_email
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from rest_framework.decorators import action


class PropertyViewSet(ModelViewSet):
	queryset = Property.objects.all()
	serializer_class = PropertySerializer
	permission_classes = [IsAuthenticated]
	filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
	filterset_class = PropertyFilter
	ordering_fields = ['rental_cost', 'num_units']


	def get_queryset(self):
		user = self.request.user
		if user.is_anonymous:
			return Property.objects.none()
		return Property.objects.filter(owner=user)
	
	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)


class TenantViewSet(ModelViewSet):
	queryset = Tenant.objects.all()
	serializer_class = TenantSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.is_anonymous:
			return Property.objects.none()
		return Tenant.objects.filter(property__owner=user)
	
	def perform_create(self, serializer):
		property_id = self.request.data.get('property')
		user = self.request.user

		try:
			Property.objects.get(id=property_id, owner=user)
		except Property.DoesNotExist:
			raise serializers.ValidationError('You do not own this property')

		if Tenant.objects.filter(property_id=property_id).exists():
			raise serializers.ValidationError('This property already has a tenant')
		serializer.save()
	
	def perform_update(self, serializer):
		serializer.save()
	
	def perform_destroy(self, instance):
		instance.delete()

class PaymentViewSet(ModelViewSet):
	queryset = Payment.objects.all()
	serializer_class = PaymentSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.is_anonymous:
			return Property.objects.none()
        # Filter payments where the tenant's property is managed by the current user
		return Payment.objects.filter(tenant__property__owner=user)

	def perform_create(self, serializer):
		tenant_id = self.request.data.get('tenant')
		user = self.request.user

		try:
			Tenant.objects.get(id=tenant_id, property__owner=user)
		except Tenant.DoesNotExist:
			raise serializers.ValidationError('This tenant is not managed by you')
		serializer.save()

	def perform_update(self, serializer):
		serializer.save()

	def perform_destroy(self, instance):
		instance.delete()

	#send payment reminders to tenants whose payments are due in the next 15 days
	@action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
	def reminder(user, request):
		user = request.user

		today = timezone.now().date()
		payments_due_soon = Payment.objects.filter(
			tenant__property__owner=user,
			due_date__gte=today,
			due_date__lte=today + timedelta(days=15),
			is_settled=False
		)

		for payment in payments_due_soon:
			send_payment_notification_email(payment.tenant, payment)
		return Response({'message': 'Payment reminders sent successfully'}, status=status.HTTP_200_OK)

