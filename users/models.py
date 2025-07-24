#users/models.py

from django.db import models
import string
import random

def generate_invite_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class UserProfile(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    invite_code = models.CharField(max_length=6, unique=True, default=generate_invite_code)
    invited_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='invited_users')
    activated_invite = models.BooleanField(default=False)

    def __str__(self):
        return self.phone_number
