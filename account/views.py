# From Django
from django.contrib.auth.models import User

# From rest_framework
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

# From 3rd party
from knox.models import AuthToken

# From Project
from account.models import Profile
from account.pagination import ProfilePageNumberPagination
from account.serializers import UserSerializer, RegisterSerializer, LoginSerializer, UserDetailSerializer, \
    ProfileSerializer, ProfileDetailSerializer
from core.permissions import IsOwnerOrReadOnly
from notification.models import Follower
from notification.serializers import followerDetailsSerializer
from post.models import ImagePost
from post.serializers import ImagePostSerializer


class RegisterAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    # Register API
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(data={
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]},
            status=status.HTTP_201_CREATED)


class LoginAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    # Login API
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        _, token = AuthToken.objects.create(user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token
        }, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    # permission_classes = [AllowAny]
    pagination_class = ProfilePageNumberPagination

    # User profile page
    def retrieve(self, request, pk=None):
        user = get_object_or_404(User.objects.all(), pk=pk)
        y = Profile.objects.follow_me(user=user)
        print(y)

        return Response(data={'user_details': UserDetailSerializer(user).data,
                              'user_posts': ImagePostSerializer(ImagePost.objects.filter(author=user), many=True).data,
                              'Followers': ProfileDetailSerializer(y, many=True).data,
                              'Following': ProfileDetailSerializer(Profile.objects.follow_them(user=user),
                                                                   many=True).data,
                              }, status=HTTP_200_OK)

    def partial_update(self, request, pk=None, *args, **kwargs):
        instance = Profile.objects.filter(user=get_object_or_404(User.objects.all(), pk=pk)).first()
        serializer = ProfileSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def destroy(self, request, pk=None, *args, **kwargs):
        with transaction.atomic():
            instance = Profile.objects.filter(user=get_object_or_404(User.objects.all(), pk=pk)).first()
            instance.is_active = False
            instance.user.is_active = False
            instance.save()
            instance.user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
