# users/urls.py



from django.urls import path
from .views import RequestCodeView, VerifyCodeView, UserProfileView, ActivateInviteCodeView

urlpatterns = [
    path('auth/request-code/', RequestCodeView.as_view()),
    path('auth/verify-code/', VerifyCodeView.as_view()),
    path('profile/', UserProfileView.as_view()),
    path('profile/activate-invite/', ActivateInviteCodeView.as_view()),
]
