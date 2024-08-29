from rest_framework.viewsets import ModelViewSet
from .models import Property, Tenant, Payment
from .serializers import PropertySerializer, TenantSerializer, PaymentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

class PropertyViewSet(ModelViewSet):
	queryset = Property.objects.all()
	serializer_class = PropertySerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		return Property.objects.filter(owner=user)
	
	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)


class TenantViewSet(ModelViewSet):
	queryset = Tenant.objects.all()
	serializer_class = TenantSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
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
        # Filter payments where the tenant's property is managed by the current user
        return Payment.objects.filter(tenant__property__owner=user)

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()