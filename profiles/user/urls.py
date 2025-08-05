# 

from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.CurrentUserProfileAPIView.as_view(), name='current_user_profile_api'),
    path('profile/create/', views.UserProfileCreateAPIView.as_view(), name='create_user_profile_api'),
    path('profile/<int:pk>/', views.UserProfileRetrieveAPIView.as_view(), name='view_user_profile_api'),
    path('profile/<int:pk>/delete/', views.UserProfileDeleteAPIView.as_view(), name='delete_user_profile_api'),
    path('profile/<int:pk>/update-phone/', views.UserProfileUpdatePhoneAPIView.as_view(), name='update_phone_number_api'),
    path('firebase-login/', views.FirebaseLoginAPIView.as_view(), name='firebase_login_api'),
    path('reset-password/', views.UserProfilePasswordResetAPIView.as_view(), name='reset_password_api'),
]
