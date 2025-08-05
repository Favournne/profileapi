# permissions.py
from rest_framework import permissions
from .firebase_utils import verify_firebase_id_token
from .models import CustomUser
import logging

logger = logging.getLogger(__name__)

class IsFirebaseAuthenticated(permissions.BasePermission):
    """
    Verifies Firebase ID token from Authorization header and sets:
    - request.firebase_user (decoded token)
    - request.user (CustomUser instance)
    """

    def has_permission(self, request, view):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')

        if not auth_header.startswith('Bearer '):
            logger.warning("Missing or invalid Authorization header.")
            return False

        id_token = auth_header[7:]  # Remove "Bearer "

        try:
            decoded_token = verify_firebase_id_token(id_token)
            request.firebase_user = decoded_token

            uid = decoded_token.get('uid')
            if not uid:
                logger.warning("Decoded Firebase token missing UID.")
                return False

            user = CustomUser.objects.filter(firebase_uid=uid).first()
            if user:
                request.user = user  # Set request.user
                return True
            else:
                logger.warning(f"No CustomUser found for UID: {uid}")
                return False

        except Exception as e:
            logger.error(f"Firebase authentication failed: {e}")
            return False
