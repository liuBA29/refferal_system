from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import UserProfile

class PhoneNumberAuthentication(BaseAuthentication):
    def authenticate(self, request):
        phone_number = request.headers.get('X-Phone-Number')
        if not phone_number:
            return None  # дальше пускает анонимных

        try:
            user = UserProfile.objects.get(phone_number=phone_number)
        except UserProfile.DoesNotExist:
            raise AuthenticationFailed('User not found')

        return (user, None)
