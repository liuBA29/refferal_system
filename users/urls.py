from django.urls import path
from .views import *


urlpatterns = [
    path('send_phone/', SendPhoneView.as_view(), name='send_phone'),
    path('verify_code/', VerifyCodeView.as_view(), name='verify_code'),
    path('profile/', profile_view),
]
