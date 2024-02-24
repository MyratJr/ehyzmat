from rest_framework import serializers
from .models import OTP


class OTPSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(read_only=True)

    class Meta:
        model = OTP
        fields = ('phone', 'otp')