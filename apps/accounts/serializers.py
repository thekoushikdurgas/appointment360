"""
Serializers for authentication and user management
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import AdminUser


class LoginSerializer(serializers.Serializer):
    """Serializer for login"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid email or password.')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must provide email and password.')
        return attrs


class AdminUserSerializer(serializers.ModelSerializer):
    """Serializer for AdminUser model"""
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = AdminUser
        fields = [
            'id', 'username', 'email', 'name', 'role', 'is_active',
            'download_limit', 'column_allowed', 'last_login', 'date_joined',
            'created_by'
        ]
        read_only_fields = ['last_login', 'date_joined']


class PasswordResetSerializer(serializers.Serializer):
    """Serializer for password reset"""
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer for password reset confirmation"""
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)
    confirm_password = serializers.CharField(min_length=8)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs

