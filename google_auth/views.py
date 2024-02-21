from .services import createJwtToken
from django.shortcuts import redirect
from django.conf import settings
from rest_framework.views import APIView
from .serializers import AuthSerializer

class GoogleLoginApi(APIView):
    def get(self, request, *args, **kwargs):
        auth_serializer = AuthSerializer(data=request.GET)
        auth_serializer.is_valid(raise_exception=True)
        
        validated_data = auth_serializer.validated_data
        print(validated_data)
        user_data, jwt_token = createJwtToken(validated_data)
        
        response = redirect(settings.BASE_APP_URL)
        response.set_cookie('Your_access_token', jwt_token, max_age = 60 * 24 * 60 * 60)
        return response
    
    def post(self, request, *args, **kwargs):
        pass