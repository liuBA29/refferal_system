#users/serializers.py

from rest_framework import serializers
from .models import User, PhoneCode
from django.contrib.auth.hashers import make_password
import random
import string


class UserProfileSerializer(serializers.ModelSerializer):
    activated_invite = serializers.SerializerMethodField()
    invited_users = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('phone', 'invite_code', 'activated_invite', 'invited_users')

    def get_activated_invite(self, obj):
        return obj.activated_invite.invite_code if obj.activated_invite else None

    def get_invited_users(self, obj):
        users = User.objects.filter(activated_invite=obj)
        return [user.phone for user in users]



class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField()


class CodeVerifySerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()
    invite_code = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        phone = data.get("phone")
        code = data.get("code")

        try:
            phone_code = PhoneCode.objects.get(phone=phone)
        except PhoneCode.DoesNotExist:
            raise serializers.ValidationError("Код не запрошен")

        if phone_code.code != code:
            raise serializers.ValidationError("Неверный код")

        return data

    def create(self, validated_data):
        phone = validated_data["phone"]
        invite_code = validated_data.get("invite_code")

        user, created = User.objects.get_or_create(phone=phone)

        if created:
            # Только если пользователь создан впервые — обрабатываем инвайт
            if invite_code:
                try:
                    referrer = User.objects.get(invite_code=invite_code)
                    user.referred_by = referrer
                    user.save()
                except User.DoesNotExist:
                    pass  # неверный invite_code — игнорируем
        return user


