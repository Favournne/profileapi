# --- user/urls.py ---
from django.urls import path
from . import views

lookup_field = 'pk'

urlpatterns = [
    path('profile/', views.UserProfileCreateAPIView.as_view(), name='create_user_profile_api'),
    path('profile/<int:pk>/', views.UserProfileRetrieveAPIView.as_view(), name='view_user_profile_api'),
    path('profile/<int:pk>/delete/', views.UserProfileDeleteAPIView.as_view(), name='delete_user_profile_api'),
    path('profile/<int:pk>/update-phone/', views.UserProfileUpdatePhoneAPIView.as_view(), name='update_phone_number_api'),
    path('login/', views.UserLoginAPIView.as_view(), name='user_login_api'),

    path('reset-password/', views.UserProfilePasswordResetAPIView.as_view(), name='reset_password_api'),
]
   