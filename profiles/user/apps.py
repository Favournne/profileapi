import firebase_admin
from firebase_admin import credentials
from django.apps import AppConfig
import os

class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "user"

    def ready(self):
        
        if not firebase_admin._apps:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            # Construct the full path to the Firebase credential file
            cred_path = os.path.join(base_dir, 'profiles', 'profiles', 'firebase_credentials.json')

            # Initialize Firebase
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
