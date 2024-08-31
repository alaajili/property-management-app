from django.db import models
from users.models import CustomUser
from django.utils import timezone

class Property(models.Model):
	PROPERTY_TYPES = (
		('House', 'House'),
		('Apartment', 'Apartment'),
		('Commercial', 'Commercial'),
		('Other', 'Other')
	)
	name = models.CharField(max_length=50)
	address = models.CharField(max_length=100)
	property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
	num_units = models.IntegerField(default=1)
	rental_cost = models.DecimalField(max_digits=10, decimal_places=2)
	owner = models.ForeignKey(CustomUser, related_name='properties', on_delete=models.CASCADE)

	def __str__(self):
		return self.name

class Tenant(models.Model):
	property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name='tenant')
	name = models.CharField(max_length=50)
	email = models.EmailField()
	phone_number = models.CharField(max_length=15)
	section = models.CharField(max_length=50)

	def __str__(self):
		return self.tenant.email
	

class Payment(models.Model):
	tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='payments')
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	due_date = models.DateField(default=timezone.now)
	is_settled = models.BooleanField(default=False)

	def __str__(self):
		return f"{self.tenant.email} has a payment of {self.amount} due on {self.due_date}"
