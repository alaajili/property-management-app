from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Property, Tenant, Payment
from django.utils import timezone
from datetime import timedelta
from users.models import CustomUser
import time

class UserTests(APITestCase):

	def setUp(self):
		self.register_url = reverse('register')
		self.login_url = reverse('login')
		timestamp = int(time.time())
		self.user_data = {
			'email': f'testuser{timestamp}@example.com',
			'username': f'testuser{timestamp}',
			'firstname': 'Test',
			'lastname': 'User',
			'password': 'password123',
        }

	def test_user_registration(self):
		response = self.client.post(self.register_url, self.user_data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_user_login(self):
		self.client.post(self.register_url, self.user_data)
		response = self.client.post(self.login_url, {
			'email': self.user_data['email'],
			'password': self.user_data['password']
		})
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertIn('access', response.data)
		self.token = response.data['access']

	def authenticate(self):
		self.test_user_login()
		self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

class PropertyTests(UserTests):

    def setUp(self):
        super().setUp()
        self.property_url = reverse('property-list')

    def test_create_property(self):
        self.authenticate()
        property_data = {
            'name': 'Test Property',
            'address': '123 Test St',
            'property_type': 'House',
            'num_units': 1,
            'rental_cost': '1500.00'
        }
        response = self.client.post(self.property_url, property_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_properties(self):
        self.authenticate()
        response = self.client.get(self.property_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TenantTests(UserTests):

	def setUp(self):
		super().setUp()
		self.tenant_url = reverse('tenant-list')

	def test_create_tenant(self):
		self.authenticate()
		self.property = Property.objects.create(
            name='Test Property',
            address='123 Test St',
            property_type='House',
            num_units=1,
            rental_cost='1500.00',
            owner=CustomUser.objects.get(email=self.user_data['email'])
        )
		tenant_data = {
            'property': self.property.id,
            'name': 'Test Tenant',
            'email': 'tenant@example.com',
            'phone_number': '1234567890',
            'section': 'A'
        }
		response = self.client.post(self.tenant_url, tenant_data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_get_tenants(self):
		self.authenticate()
		response = self.client.get(self.tenant_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
             

class PaymentTests(UserTests):

	def setUp(self):
		super().setUp()
		self.payment_url = reverse('payment-list')

	def test_create_payment(self):
		self.authenticate()
		self.property = Property.objects.create(
            name='Test Property',
            address='123 Test St',
            property_type='House',
            num_units=1,
            rental_cost='1500.00',
            owner=CustomUser.objects.get(email=self.user_data['email'])

        )
		self.tenant = Tenant.objects.create(
            property=self.property,
            name='Test Tenant',
            email='tenant@example.com',
            phone_number='1234567890',
            section='A'
        )
		payment_data = {
            'tenant': self.tenant.id,
            'amount': '1500.00',
            'due_date': timezone.now().date(),
            'is_settled': False
        }
		response = self.client.post(self.payment_url, payment_data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_payment_reminder(self):
		self.authenticate()
		self.property = Property.objects.create(
            name='Test Property',
            address='123 Test St',
            property_type='House',
            num_units=1,
            rental_cost='1500.00',
            owner=CustomUser.objects.get(email=self.user_data['email'])

        )
		self.tenant = Tenant.objects.create(
            property=self.property,
            name='Test Tenant',
            email='tenant@example.com',
            phone_number='1234567890',
            section='A'
        )
		Payment.objects.create(
            tenant=self.tenant,
            amount='1500.00',
            due_date=timezone.now().date() + timedelta(days=5),
            is_settled=False
        )
		reminder_url = reverse('payment-reminder')
		response = self.client.get(reminder_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['message'], 'Payment reminders sent successfully')
