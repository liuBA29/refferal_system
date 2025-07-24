#users/views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny  # добавим
from .models import UserProfile
from .tokens import send_code, verify_code
from .serializers import RequestCodeSerializer, VerifyCodeSerializer, UserProfileSerializer

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, get_object_or_404
from .models import UserProfile


def profile_page(request):
    # Пока просто для примера возьмём первый профиль в базе
    user_profile = UserProfile.objects.first()

    # Можно сделать проверку, если профиля нет
    if not user_profile:
        context = {"error": "Профиль пользователя не найден."}
        return render(request, "users/profile.html", context)

    # Получаем список телефонов приглашённых пользователей
    invited_phones = user_profile.invited_users.values_list('phone_number', flat=True)

    context = {
        "user_profile": user_profile,
        "invited_phones": invited_phones,
    }
    return render(request, "users/profile.html", context)


class UserProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        phone_number = request.headers.get("X-Phone-Number")
        if not phone_number:
            return Response(
                {"detail": "Phone number header missing."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            profile = UserProfile.objects.get(phone_number=phone_number)
        except UserProfile.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)


class ActivateInviteCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.headers.get("X-Phone-Number")  # ✅ получаем номер

        if not phone_number:
            return Response(
                {"detail": "Phone number header missing."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = UserProfile.objects.get(phone_number=phone_number)  # ✅ получаем user-профиль
        except UserProfile.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        code_to_activate = request.data.get('invite_code')

        if not code_to_activate:
            return Response(
                {"detail": "Invite code is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if user.invited_by is not None:
            return Response(
                {"detail": "Invite code already activated"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            inviter = UserProfile.objects.get(invite_code=code_to_activate)
        except UserProfile.DoesNotExist:
            return Response(
                {"detail": "Invite code does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.invited_by = inviter
        user.save()

        return Response({"detail": "Invite code activated successfully"})


class RequestCodeView(APIView):
    def post(self, request):
        serializer = RequestCodeSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone_number']
            send_code(phone)
            return Response({'detail': 'Verification code sent (simulated).'}, status=200)
        return Response(serializer.errors, status=400)

class VerifyCodeView(APIView):
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone_number']
            code = serializer.validated_data['code']

            if not verify_code(phone, code):
                return Response({'detail': 'Invalid code'}, status=400)

            user, created = UserProfile.objects.get_or_create(phone_number=phone)
            return Response({'detail': 'Login successful', 'user': UserProfileSerializer(user).data})
        return Response(serializer.errors, status=400)
