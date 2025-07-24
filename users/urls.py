# users/urls.py



from django.urls import path
from .views import RequestCodeView, VerifyCodeView, UserProfileView, ActivateInviteCodeView, profile_page


app_name="users"
urlpatterns = [
    # path('auth/request-code/', RequestCodeView.as_view()),
    # path('auth/verify-code/', VerifyCodeView.as_view()),
    # path('api/profile/', UserProfileView.as_view()),
    path('profile/', profile_page, name='profile_page'),
    # path('profile/activate-invite/', ActivateInviteCodeView.as_view()),
]
