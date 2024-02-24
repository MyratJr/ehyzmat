from django.db import models
from advertisement.views import phone_regex
from datetime import timedelta, datetime


class OTP(models.Model):
    phone = models.CharField(validators=[phone_regex], max_length=12)
    otp = models.IntegerField()
    is_verified = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
    expired_at = models.DateTimeField()