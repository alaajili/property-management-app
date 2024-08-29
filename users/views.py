from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer

class RegisterView(CreateAPIView):
	queryset = CustomUser.objects.all()
	authentication_classes = ([])
	permission_classes = [AllowAny]
	serializer_class = RegisterSerializer


class LoginView(GenericAPIView):
	serializer_class = LoginSerializer
	authentication_classes = ([])
	permission_classes = [AllowAny]

	def post(self, request):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data
		tokens = serializer.get_tokens(user)
		return Response(tokens, status=status.HTTP_201_CREATED)