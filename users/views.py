#users/views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny  # добавим
from .models import UserProfile
from .tokens import send_code, verify_code
from .serializers import RequestCodeSerializer, VerifyCodeSerializer, UserProfileSerializer
from django.contrib import messages
import time
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile


def home_page(request):
    if request.method == "POST":
        phone = request.POST.get("phone_number")
        if phone:
            send_code(phone)  # псевдо-отправка кода
            request.session["auth_phone"] = phone
            time.sleep(1.5)  # имитация задержки
            return redirect("users:verify_code")
        else:
            messages.error(request, "Введите номер телефона.")
    return render(request, "users/home.html")


def verify_code_page(request):
    phone = request.session.get("auth_phone")
    if not phone:
        return redirect("home")

    if request.method == "POST":
        code = request.POST.get("code")
        if verify_code(phone, code):
            user, created = UserProfile.objects.get_or_create(phone_number=phone)
            messages.success(request, "Успешный вход.")
            return redirect("users:profile_page")
        else:
            messages.error(request, "Неверный код.")

    return render(request, "users/verify.html", {"phone": phone})



def profile_page(request):
    phone = request.session.get("auth_phone")
    if not phone:
        return redirect("users:home")

    user_profile = UserProfile.objects.filter(phone_number=phone).first()

    if not user_profile:
        context = {"error": "Профиль пользователя не найден."}
        return render(request, "users/profile.html", context)

    # ✅ Обработка формы активации кода
    if request.method == "POST":
        invite_code = request.POST.get("invite_code")
        if invite_code:
            if user_profile.invited_by:
                messages.error(request, "Инвайт-код уже был активирован.")
            else:
                try:
                    inviter = UserProfile.objects.get(invite_code=invite_code)
                    if inviter == user_profile:
                        messages.error(request, "Нельзя ввести свой собственный код.")
                    else:
                        user_profile.invited_by = inviter
                        user_profile.save()
                        messages.success(request, "Инвайт-код успешно активирован.")
                except UserProfile.DoesNotExist:
                    messages.error(request, "Инвайт-код не найден.")
        else:
            messages.error(request, "Введите код.")

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
