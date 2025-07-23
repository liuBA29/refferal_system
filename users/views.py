from django.shortcuts import render

import random
import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import PhoneSerializer, CodeVerifySerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    serializer = UserProfileSerializer(user)
    return Response(serializer.data)



class SendPhoneView(APIView):
    def post(self, request):
        serializer = PhoneSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            code = str(random.randint(1000, 9999))

            user, created = User.objects.get_or_create(phone=phone)
            user.auth_code = code
            user.save()

            # Имитация задержки (будто отправка СМС)
            time.sleep(1.5)
            print(f"🐰 Код авторизации для {phone}: {code}")

            return Response({"message": "Код отправлен!"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyCodeView(APIView):
    def post(self, request):
        serializer = CodeVerifySerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            code = serializer.validated_data['code']

            try:
                user = User.objects.get(phone=phone)
                if user.auth_code == code:
                    user.is_verified = True
                    user.auth_code = None
                    user.save()
                    return Response({"message": "Проверка прошла успешно", "invite_code": user.invite_code})
                else:
                    return Response({"error": "Неверный код"}, status=400)
            except User.DoesNotExist:
                return Response({"error": "Пользователь не найден"}, status=404)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
