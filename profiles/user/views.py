from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import CustomUser
from .serializers import UserProfileSerializer, PasswordResetSerializer, UserProfileCreateSerializer, UserProfileUpdateSerializer,PasswordResetSerializer
import firebase_admin

from .firebase_utils import verify_firebase_id_token  # <-- Make sure this exists
from user.permissions import IsFirebaseAuthenticated



class UserProfileRetrieveAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsFirebaseAuthenticated]


class FirebaseLoginAPIView(APIView):
    def post(self, request):
        id_token = request.data.get('id_token')
        if not id_token:
            return Response({'error': 'ID token required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user_info = verify_firebase_id_token(id_token)
            return Response({
                'message': 'Login successful.',
                'uid': user_info.get('uid'),
                'email': user_info.get('email'),
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileCreateAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileCreateSerializer

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

