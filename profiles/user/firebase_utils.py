import firebase_admin
from firebase_admin import credentials, auth
import os
import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


logger = logging.getLogger(__name__)

# Path to your Firebase credentials JSON
FIREBASE_CRED_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'firebase_credentials.json')
try:
    # Initialize Firebase Admin SDK with credentials
    if not firebase_admin._apps:
        logger.debug(f"Loading Firebase credentials from: {FIREBASE_CRED_PATH}")
        cred = firebase_admin.credentials.Certificate(FIREBASE_CRED_PATH)
        firebase_admin.initialize_app(cred)
except Exception as e:
    logger.error(f"Failed to initialize Firebase Admin SDK: {str(e)}")
    raise

# Function to verify Firebase ID Token and email verification status
def verify_firebase_id_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        logger.debug(f"Decoded Firebase token: {decoded_token}")

        # 🚫 Check if the user's email has been verified, commenting to temporarly bypass email verification
        # if not decoded_token.get('email_verified'):
        #     raise ValueError("Email not verified. Please verify your email before continuing.")

        return decoded_token

    except Exception as e:
        raise ValueError(f"Invalid Firebase ID token: {e}")

def custom_exception_handler(exc, context):
    """
    Custom exception handler to return a more user-friendly error response.
    """
    response = exception_handler(exc, context)
    if response is None:
        return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response