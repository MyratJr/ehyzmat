from rest_framework import generics, permissions, mixins, viewsets
from services.serializers import HomeServicesSerializers
from ratings.models import Like_User, View_User, Rate_User
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from services.models import Service
from .serializers import *
from .models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status
from otp.models import OTP
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data["phone"]
        temporary_otp = get_object_or_404(OTP, phone=phone)
        otp = serializer.validated_data["otp"]
        if temporary_otp.otp == otp and temporary_otp.is_expired is False:
            temporary_otp.is_verified = True
            temporary_otp.save()
            user = serializer.save()
            refresh = RefreshToken.for_user(User.objects.get(id=user.id))
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })
        return Response("OTP is wrong or has expired", status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
        serializer_class = ChangePasswordSerializer
        permission_classes = (IsAuthenticated,)

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj
        
        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                if not self.object.check_password(serializer.data.get("old_password")) or len(serializer.data.get("new_password"))<8:
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                }
                return Response(response)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeForgotPassword(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser]
    queryset = User.objects.all()

    def partial_update(self, request, pk, *args, **kwargs):
        kwargs['partial'] = True
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        otp = data.get("otp")
        phone = data.get("phone")
        password = data.get("password")
        if len(password)<8:
             raise serializers.ValidationError({
                        'new_password': 'Password must be at least 8 characters long.'})
        saved_otp = get_object_or_404(OTP, phone=phone)
        if saved_otp.otp == otp and saved_otp.is_expired is False:
            saved_otp.is_verified = True
            user_change_password = User.objects.get(pk=pk)
            user_change_password.set_password(password)
            user_change_password.save()
            saved_otp.save()
            return Response({"success"})
        raise serializers.ValidationError({"detail":"Your OTP is wrong or has expired"})


class LoginAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(User.objects.get(id=user.id))
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })
        # login(request, user)
        # return super(LoginAPI, self).post(request, format=None)
    

class UpdateUserAPIView(mixins.UpdateModelMixin,
                        generics.GenericAPIView
                        ):
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer
    parser_classes = [MultiPartParser,FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class GetUsersAPIView(mixins.ListModelMixin,
                    generics.GenericAPIView
                    ):
    queryset = User.objects.all()
    serializer_class = GetUsersSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class User_CategoriesAPIView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserViewSerializers
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        services = Service.objects.filter(user=instance)
        if request.user and request.user.is_authenticated:
            service, created = View_User.objects.get_or_create(viewing_user=request.user, viewed_user=instance)
            if created:
                instance.view_counter = instance.view_counter + 1
                instance.save()
        new_data = [{
                    "User_data": serializer.data,
                    # "Liked_number": Like_User.objects.filter(favorited_user=instance).count(),
                    # "Viewed_number": View_User.objects.filter(viewed_user=instance).count(),
                    },{
                    "User_services": HomeServicesSerializers(services, many=True).data,
                    }]
        return Response(new_data)
    


class LikeUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        liked_user = get_object_or_404(User, pk=pk)
        print(request.user.username)
        user, created = Like_User.objects.get_or_create(favoriting_user=request.user,favorited_user=liked_user)
        if created:
            liked_user.like_counter += 1
            liked_user.save()
        return Response({"success": True, "likes": liked_user.like_counter})


class LikeToUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rated_objects = Rate_User.objects.filter(rated_user=request.user)
        liked_objects = Like_User.objects.filter(favorited_user=request.user)
        liked_services = Like_Service.objects.filter(service__user=request.user).select_related("user", "service")
        rated_serializer = RateSerializer(rated_objects, many=True)
        liked_serializer = LikedUsersSerializer(liked_objects, many=True)
        liked_sevices_serializer = LikedServiceSerializer(liked_services, many=True)
        return Response({
            "rated": rated_serializer.data,
            "liked": liked_serializer.data,
            "liked_services": liked_sevices_serializer.data,
        }, status=status.HTTP_200_OK)
    

class LikeOfUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rated_objects = Rate_User.objects.filter(rating_user=request.user)
        liked_objects = Like_User.objects.filter(favoriting_user=request.user)
        liked_services = Like_Service.objects.filter(user=request.user).select_related("user", "service")
        rated_serializer = RateOfUserSerializer(rated_objects, many=True)
        liked_serializer = LikedUsersSerializer(liked_objects, many=True)
        liked_sevices_serializer = LikedServiceSerializer(liked_services, many=True)
        return Response({
            "rated": rated_serializer.data,
            "liked": liked_serializer.data,
            "liked_services": liked_sevices_serializer.data,
        }, status=status.HTTP_200_OK)