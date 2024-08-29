from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomUser
		fields = ['email', 'username', 'firstname', 'lastname', 'password']
		extra_kwargs = {
			'password': {'write_only': True, 'min_length': 6, 'max_length': 68}
		}
	
	def create(self, validated_data):
		user = CustomUser.objects.create_user(
			email=validated_data['email'],
			username=validated_data['username'],
			firstname=validated_data['firstname'],
			lastname=validated_data['lastname'],
			password=validated_data['password']
		)
		return user


class LoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField(
		max_length=68, min_length=6, write_only=True
	)

	def validate(self, data):
		email = data.get('email')
		password = data.get('password')
		user = authenticate(email=email, password=password)
		if not user:
			raise serializers.ValidationError('Invalid credentials')
		return user

	def get_tokens(self, user):
		refresh = RefreshToken.for_user(user)
		return {
			'refresh': str(refresh),
			'access': str(refresh.access_token)
		}

	