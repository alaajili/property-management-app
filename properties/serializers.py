from rest_framework import serializers
from .models import Property, Tenant, Payment



class PaymentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Payment
		fields = '__all__'
class TenantSerializer(serializers.ModelSerializer):
	payments = PaymentSerializer(many=True, read_only=True)
	class Meta:
		model = Tenant
		fields = '__all__'

class PropertySerializer(serializers.ModelSerializer):
	tenant = TenantSerializer(read_only=True)
	class Meta:
		model = Property
		fields = '__all__'
		read_only_fields = ['owner']
