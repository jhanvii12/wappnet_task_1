from django.shortcuts import render

# Create your views here.
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, CustomTokenObtainPairSerializer

User = get_user_model()

# Registration View
class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]  # Anyone can register

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User registered successfully', 'user_id': user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login View using JWT
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer


# Get All Users View
class UserListAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can see the list of users

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


# Change Password View
class UserChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can change their password

    def post(self, request):
        user = request.user
        password = request.data.get('password')
        if password:
            user.set_password(password)  # Hash the password
            user.save()  # Save the user with the new password
            return Response({'message': 'Password changed successfully'})
        return Response({'error': 'Password not provided'}, status=status.HTTP_400_BAD_REQUEST)

