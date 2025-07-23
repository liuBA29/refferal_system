from django.db import models
import random
import string

def generate_invite_code():
    """Функция создаёт случайный 6-значный код из букв и цифр"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class User(models.Model):
    phone = models.CharField(max_length=15, unique=True)
    auth_code = models.CharField(max_length=4, blank=True, null=True)  # код для входа
    is_verified = models.BooleanField(default=False)  # подтвердил ли код
    invite_code = models.CharField(max_length=6, unique=True, default=generate_invite_code)
    referred_by = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='referrals'
    )

    def __str__(self):
        return self.phone

