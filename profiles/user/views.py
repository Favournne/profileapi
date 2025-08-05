from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import CustomUser
from .serializers import (
    UserProfileSerializer,
    PasswordResetSerializer,
    UserProfileCreateSerializer
)
from .permissions import IsFirebaseAuthenticated
from .firebase_utils import verify_firebase_id_token
import logging

# Setup logging
logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class UserProfileCreateAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileCreateSerializer

    def create(self, request, *args, **kwargs):
        try:
            logger.debug(f"Raw request data: {dict(request.data)}")
            auth_header = request.headers.get('Authorization', '')
            logger.debug(f"Authorization header: {auth_header}")
            if not auth_header.startswith('Bearer '):
                logger.error("Missing or invalid Authorization header")
                return Response({'error': 'Authorization header missing or invalid.'}, status=status.HTTP_401_UNAUTHORIZED)

            id_token = auth_header.split(' ')[1]
            try:
                user_info = verify_firebase_id_token(id_token)
                logger.debug(f"User info: {user_info}")
            except Exception as e:
                logger.error(f"Token verification failed: {str(e)}")
                return Response({'error': f"Invalid Firebase ID token: {str(e)}"}, status=status.HTTP_401_UNAUTHORIZED)

            # Validate required fields
            required_fields = ['first_name', 'last_name', 'phone_number', 'password', 'retype_password']
            missing_fields = [field for field in required_fields if field not in request.data or not request.data[field]]
            if missing_fields:
                logger.error(f"Missing required fields: {missing_fields}")
                return Response({'error': f"Missing required fields: {missing_fields}"}, status=status.HTTP_400_BAD_REQUEST)

            data = request.data.copy()
            data['firebase_uid'] = user_info['uid']
            data['email'] = user_info.get('email', '')
            logger.debug(f"Modified request data: {data}")
            instance = CustomUser.objects.filter(firebase_uid=data['firebase_uid']).first()

            serializer = self.get_serializer(data=data, instance=instance)
            try:
                serializer.is_valid(raise_exception=True)
            except Exception as e:
                logger.error(f"Serializer validation failed: {str(e)}", exc_info=True)
                return Response({'error': f"Invalid data: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                instance = CustomUser.objects.get(firebase_uid=data['firebase_uid'])
                instance.email = data.get('email', instance.email)
                instance.first_name = data.get('first_name', instance.first_name)
                instance.last_name = data.get('last_name', instance.last_name)
                
                if password := data.get('password'):
                    instance.set_password(password)
                instance.save()
            except CustomUser.DoesNotExist:
                instance = CustomUser.objects.create_user(**data)
            except Exception as e:
                logger.error(f"Error occurred while creating user profile: {str(e)}", exc_info=True)
                return Response({'error': f"Failed to create user profile: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            serializer = self.get_serializer(instance)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Unexpected error in UserProfileCreateAPIView: {str(e)}", exc_info=True)
            return Response({'error': f"Server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CurrentUserProfileAPIView(generics.RetrieveAPIView):
    """
    GET /api/user/profile/
    Returns the authenticated Firebase user's profile using firebase_uid.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsFirebaseAuthenticated]

    def get_object(self):
        firebase_uid = self.request.firebase_user.get('uid')  # Provided by IsFirebaseAuthenticated permission
        return get_object_or_404(CustomUser, firebase_uid=firebase_uid)

@method_decorator(csrf_exempt, name='dispatch')
class FirebaseLoginAPIView(APIView):
    def post(self, request):
       #logger.debug("FirebaseLoginAPIView disabled for debugging")
        #return Response({'error': 'Endpoint disabled for debugging'}, status=status.HTTP_403_FORBIDDEN)"""
        # Original code commented out to prevent partial user creation
        logger.debug(f"Firebase login request data: {request.data}")
        id_token = request.data.get('id_token')
        if not id_token:
            logger.error("No ID token provided")
            return Response({'error': 'ID token required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            logger.debug("Attempting to verify Firebase token")
            user_info = verify_firebase_id_token(id_token)
            logger.debug(f"Token verified successfully: {user_info}")


            uid = user_info['uid']
            email = user_info.get('email')
            name = user_info.get('name', '')
            first_name = name.split()[0] if name else ''

            
            logger.debug(f"Creating/getting user with UID: {uid}")
            user, created = CustomUser.objects.get_or_create(
                firebase_uid=uid,
                defaults={
                    'email': email,
                    'first_name': first_name,
                }
            )

            response_data={
                'message': 'Login successful.',
                'uid': uid,
                'email': email,
                'created': created,
            'full_name': f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
            }
            logger.debug(f"Returning success response: {response_data}")
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Firebase login error: {str(e)}", exc_info=True)
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileRetrieveAPIView(generics.RetrieveAPIView):
    """
    GET /api/user/profile/<pk>/
    Retrieves a specific user profile by pk (not necessarily the authenticated user).
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsFirebaseAuthenticated]

class UserProfileDeleteAPIView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer

@method_decorator(csrf_exempt, name='dispatch')
class UserProfilePasswordResetAPIView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class UserProfileUpdatePhoneAPIView(APIView):
    def patch(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        phone_number = request.data.get('phone_number', '').strip()

        if not phone_number:
            return Response({'phone_number': ['This field is required.']}, status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(phone_number=phone_number).exclude(pk=pk).exists():
            return Response({'phone_number': ['Phone number already exists.']}, status=status.HTTP_400_BAD_REQUEST)

        user.phone_number = phone_number
        try:
            user.full_clean()
            user.save()
            return Response({'message': 'Phone number updated successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)