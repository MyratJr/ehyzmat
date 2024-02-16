from rest_framework import generics, permissions, mixins
from services.serializers import HomeServicesSerializers
from ratings.models import Like_User, View_User, Rate_User
from rest_framework.response import Response
from django.contrib.auth import login
from services.models import Service
from knox.views import LoginView
from .serializers import *
from .models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from rest_framework import status


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"user": UserSerializer(user, context=self.get_serializer_context()).data})


class LoginAPI(LoginView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
    

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
                    "Liked_number": Like_User.objects.filter(favorited_user=instance).count(),
                    "Viewed_number": View_User.objects.filter(viewed_user=instance).count(),
                    },{
                    "User_services": HomeServicesSerializers(services, many=True).data,
                    }]
        return Response(new_data)
    


class LikeUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        liked_user = get_object_or_404(User, pk=pk)
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