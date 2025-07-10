from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from .models import CustomUser
from .serializers import UserProfileSerializer
from .serializers import PasswordResetSerializer


class UserLoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email', '').strip()
        password = request.data.get('password', '')

        if not email or not password:
            return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not registered.'}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response({'error': 'Incorrect password.'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({'message': 'Login successful.'}, status=status.HTTP_200_OK)


class UserProfileCreateAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileRetrieveAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileDeleteAPIView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer

class UserProfilePasswordResetAPIView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileUpdatePhoneAPIView(APIView):
    def patch(self, request, pk):
        user_profile = get_object_or_404(CustomUser, pk=pk)
        phone_number = request.data.get('phone_number', '').strip()
        if not phone_number:
            return Response({'phone_number': ['This field is required.']}, status=status.HTTP_400_BAD_REQUEST)
        if CustomUser.objects.filter(phone_number=phone_number).exclude(pk=pk).exists():
            return Response({'phone_number': ['Phone number already exists.']}, status=status.HTTP_400_BAD_REQUEST)
        user_profile.phone_number = phone_number
        try:
            user_profile.full_clean()
            user_profile.save()
            return Response({'message': 'Phone number updated successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
