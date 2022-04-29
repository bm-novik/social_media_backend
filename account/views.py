# From Django
from django.contrib.auth.models import User
from django.db import transaction

# From rest_framework
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

# From 3rd party
from knox.models import AuthToken

# From Project
from account.models import Profile
from account.pagination import ProfilePageNumberPagination
from account.serializers import UserSerializer, RegisterSerializer, LoginSerializer, \
    ProfileSerializer, ProfileDetailSerializer, UserPasswordUpdate, UserDetailSerializer, \
    UserProfileDetailSerializer, ProfilePictureUpdate
from core.permissions import IsOwnerOrReadOnly, IsOwnerOnly


class RegisterAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = RegisterSerializer

    # Register API
    def post(self, request, *args, **kwargs):
        data = {
            'username': request.data.get('username'),
            'email': request.data.get('email'),
            'password': request.data.get('password'),
            'confirm_password': request.data.get('confirm_password'),
            'profile': {
                'first_name': request.data.get('first_name'),
                'last_name': request.data.get('last_name'),
                'gender': request.data.get('gender'),
                'phone': request.data.get('phone'),
                'website': request.data.get('website'),
                'bio': request.data.get('bio'),
                'birth_day': request.data.get('birth_day'),
                'profile_pic': request.FILES['profile_pic']
            }
        }
        serializer = self.get_serializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(data={
            "user": UserDetailSerializer(user, context=self.get_serializer_context()).data,
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
            "user": UserDetailSerializer(user, context=self.get_serializer_context()).data,
            "token": token
        }, status=status.HTTP_200_OK)


class CheckTokenView(GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User.objects.all(), pk=request.user.pk)
        user_profile = Profile.objects.all().filter(user=user)
        if user_profile.exists():
            return Response(UserDetailSerializer(user).data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class UserPartialUpdateViewSet(viewsets.ViewSet):
    permission_classes = [IsOwnerOnly]
    http_method_names = ['patch', 'put', 'head', 'options']

    @action(detail=False, methods=['patch'])
    def info(self, request, *args, **kwargs):
        user_instance = get_object_or_404(User.objects.all(), pk=request.user.id)
        profile_instance = Profile.objects.all().filter(user=user_instance).first()

        user_serializer = UserSerializer(instance=user_instance, data=request.data.get('user'),
                                         partial=True, context={'request': request})
        profile_serializer = ProfileSerializer(instance=profile_instance, data=request.data.get('profile'),
                                               partial=True, context={'request': request})

        user_serializer.is_valid(raise_exception=True)
        profile_serializer.is_valid(raise_exception=True)

        user_serializer.save()
        profile_serializer.save()

        return Response(UserProfileDetailSerializer(user_instance).data, status=status.HTTP_206_PARTIAL_CONTENT)

    @action(detail=False, methods=['put'])
    def profile_pic(self, request, *args, **kwargs):
        user = get_object_or_404(User.objects.all(), pk=request.user.pk)
        instance = Profile.objects.all().filter(user=user).first()
        serializer = ProfilePictureUpdate(instance=instance, data={'profile_pic': request.FILES['image']},
                                          context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(UserProfileDetailSerializer(user).data, status=status.HTTP_206_PARTIAL_CONTENT)

    @action(detail=False, methods=['put'])
    def password(self, request, *args, **kwargs):
        user = get_object_or_404(User.objects.all(), pk=request.user.id)
        serializer = UserPasswordUpdate(instance=user, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(UserSerializer(user).data, status=status.HTTP_206_PARTIAL_CONTENT)


class ProfileViewSet(viewsets.ViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = ProfilePageNumberPagination

    # User profile page
    def retrieve(self, request, pk):
        return Response(UserDetailSerializer(get_object_or_404(User.objects.all(), pk=pk),
                                             context={'request': request}).data, status=HTTP_200_OK)

    @action(detail=True)
    def followers(self, request, pk):
        user = get_object_or_404(User.objects.all(), pk=pk)
        return Response(
            UserDetailSerializer(User.objects.all()
                                 .filter(profile__in=Profile.objects.follow_me(user=user)
                                         .prefetch_related('followers')),
                                 context={'request': request}, many=True).data, status=HTTP_200_OK)

    @action(detail=True)
    def following(self, request, pk):
        user = get_object_or_404(User.objects.all(), pk=pk)
        return Response(UserDetailSerializer(User.objects.all()
                                             .filter(profile__in=Profile.objects.follow_them(user=user)
                                                     .prefetch_related('followers')),
                                             context={'request': request}, many=True).data, status=HTTP_200_OK)

    @action(detail=False)
    def top_five(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.user.id)
        return Response(UserDetailSerializer(Profile.objects.top_five(user), context={'request': request},
                                             many=True).data, status=HTTP_200_OK)

    @action(detail=True)
    def profile(self, request, pk):
        return Response(UserProfileDetailSerializer(get_object_or_404(User.objects.all(), pk=pk),
                                                    context={'request': request}).data, status=HTTP_200_OK)

    def destroy(self, request, pk=None, *args, **kwargs):
        with transaction.atomic():
            instance = Profile.objects.filter(user=get_object_or_404(User.objects.all(), pk=pk)).first()
            instance.is_active = False
            instance.user.is_active = False
            instance.save()
            instance.user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
