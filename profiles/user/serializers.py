from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import re
import logging

logger = logging.getLogger(__name__)


class UserProfileCreateSerializer(serializers.ModelSerializer):
    retype_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, min_length=8, required=True)
    first_name = serializers.CharField(required=True, allow_blank=False)
    last_name = serializers.CharField(required=True, allow_blank=False)
    phone_number = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone_number', 'password', 'retype_password'
        ]

    def validate_phone_number(self, value):
        phone_regex = r'^(?:\+234|0)[789][01]\d{8}$'
        if not re.match(phone_regex, value):
            raise serializers.ValidationError("Please enter a valid Nigerian phone number.")
        return value

    def validate(self, data):
        logger.debug(f"Serializer input data: {data}")
        if data.get('password') != data.get('retype_password'):
            raise serializers.ValidationError("Passwords do not match.")
        try:
            validate_password(data['password'])
        except ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        return data

    def create(self, validated_data):
        logger.debug(f"Validated data: {validated_data}")
        validated_data.pop('retype_password')
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        try:
            user.save()
        except Exception as e:
            logger.error(f"Error occurred while saving user: {str(e)}", exc_info=True)
            raise serializers.ValidationError("Failed to create user.")
        logger.debug(f"Saved user: {user.__dict__}")
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Read-only serializer for returning user info."""
    class Meta:
        model = CustomUser
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone_number'
        ]
        read_only_fields = fields

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)  # This hashes the password!
        user.save()
        return user


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Optional serializer for updating user info (not password)."""
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number']


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        try:
            validate_password(data['new_password'])
        except ValidationError as e:
            raise serializers.ValidationError({'new_password': list(e.messages)})
        return data

    def save(self):
        email = self.validated_data['email']
        new_password = self.validated_data['new_password']
        user = CustomUser.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        return user
