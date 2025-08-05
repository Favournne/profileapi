from firebase_admin import   auth
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import CustomUser


class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise AuthenticationFailed("Missing Authorization header")

        id_token = auth_header.split(' ').pop()
        try:
             decoded_token = auth.verify_id_token(id_token)
        except Exception as e:
            raise AuthenticationFailed(f"Invalid Firebase token: {str(e)}")

        uid = decoded_token.get('uid')
        email = decoded_token.get('email')
        
        if not uid or not email:
            raise AuthenticationFailed("Invalid Firebase token payload")

        user, _ = CustomUser.objects.get_or_create(
            firebase_uid=uid,
            defaults={"email": email}
        )

        return (user, None)
