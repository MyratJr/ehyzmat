from rest_framework import status
from rest_framework.response import Response
from .serializers import OTPSerializer
from random import randint
from rest_framework import mixins, generics
from .models import OTP
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from datetime import timedelta, datetime
from users.models import User
   

class OTPView(mixins.CreateModelMixin, generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = OTPSerializer
    parser_classes = [MultiPartParser]
    queryset = OTP.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone']
        otp = randint(1000,9999)
        OTP.objects.create(phone=phone, otp=otp, expired_at=(datetime.now().replace(second=0, microsecond=0)+timedelta(minutes=5)))
        return Response({"phone":phone, "otp":otp}, status=status.HTTP_201_CREATED)
    

class ForgotPasswordView(mixins.CreateModelMixin, generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = OTPSerializer
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        try: 
            user_with_given_phone = User.objects.get(phone=phone)
        except:
            return Response({"No user found with this phone number"})
        otp = randint(1000,9999)
        OTP.objects.create(phone=phone, otp=otp, expired_at=(datetime.now().replace(second=0, microsecond=0)+timedelta(minutes=5)))
        return Response({"user_id":user_with_given_phone.id, "phone":phone, "otp":otp}, status=status.HTTP_201_CREATED)