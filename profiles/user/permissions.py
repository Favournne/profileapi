from rest_framework import permissions
from .firebase_utils import verify_firebase_id_token

class IsFirebaseAuthenticated(permissions.BasePermission):
    """
    Allows access only to users with a valid Firebase ID token.
    """

    def has_permission(self, request, view):
        id_token = request.META.get('HTTP_AUTHORIZATION')
        if not id_token:
            return False
        if id_token.startswith('Bearer '):
            id_token = id_token[7:]
        try:
            request.firebase_user = verify_firebase_id_token(id_token)
            return True
        except Exception:
            return False