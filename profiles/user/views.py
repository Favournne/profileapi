from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import CustomUser
from .serializers import UserProfileSerializer

class UserProfileCreateAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileRetrieveAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileDeleteAPIView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer

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