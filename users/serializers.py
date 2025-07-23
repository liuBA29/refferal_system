from rest_framework import serializers
from .models import User


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
