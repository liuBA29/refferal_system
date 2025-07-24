#users/serializers.py

from rest_framework import serializers
from .models import UserProfile

class RequestCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

class VerifyCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField()

class UserProfileSerializer(serializers.ModelSerializer):
    activated_code = serializers.SerializerMethodField()
    invited_users = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['phone_number', 'invite_code', 'activated_code', 'invited_users']

    def get_activated_code(self, obj):
        return obj.invited_by.invite_code if obj.invited_by else None

    def get_invited_users(self, obj):
        # Возвращаем список телефонов пользователей, которые активировали код текущего пользователя
        return [u.phone_number for u in obj.invited_users.all()]
