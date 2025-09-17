# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['full_name', 'role', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)  # مدمج مع الـ User
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'profile']
