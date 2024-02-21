from rest_framework import serializers
from users.models import User

class AuthSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=False)
    error = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = ["fullname", 'email', 'code', 'error']