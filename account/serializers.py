from django.contrib.auth.hashers import make_password, check_password
from django.db import transaction
from django.contrib.auth import authenticate

from rest_framework import serializers

from account.models import Profile
from django.contrib.auth.models import User

from core.utils import validate_unique_email, validate_password, validate_unique_username, return_data
from notification.models import Follower
from post.models import ImagePost


#######################################################################################################################
# profile
#######################################################################################################################

class ProfilePageDetailSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    post_count = serializers.SerializerMethodField()
    follow_status = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["id", 'first_name', 'last_name', 'profile_pic', 'bio', 'gender',
                  'followers_count', 'following_count', 'post_count', 'follow_status', 'website']
        read_only_fields = ["id"]

    @staticmethod
    def get_followers_count(obj):
        return Profile.objects.follow_me(user=obj.user).count()

    @staticmethod
    def get_following_count(obj):
        return Profile.objects.follow_them(user=obj.user).count()

    @staticmethod
    def get_post_count(obj):
        return ImagePost.objects.post_by_user(pk=obj.id).count()

    def get_follow_status(self, obj):
        request = self.context.get('request')
        if request:
            return Follower.objects.follow_status(observer_id=request.user.id, object_id=obj.id)
        return None


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'first_name', 'last_name', 'profile_pic', 'website', 'gender', 'phone', 'bio']
        read_only_fields = ["id"]


class ProfileDetailSerializer(serializers.ModelSerializer):
    follow_status = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'first_name', 'last_name', 'profile_pic', 'follow_status', 'website', 'gender', 'phone', 'bio']
        read_only_fields = ['id']

    def get_follow_status(self, obj):
        request = self.context.get('request')
        if request:
            return Follower.objects.follow_status(observer_id=request.user.id, object_id=obj.id)
        return None


class ProfilePictureUpdate(serializers.ModelSerializer):
    profile_pic = serializers.ImageField()

    class Meta:
        model = Profile
        fields = ['profile_pic']

    # def update(self, instance, validated_data):


#######################################################################################################################
# USER
#######################################################################################################################

class RegisterSerializer(serializers.ModelSerializer):
    profile = ProfileDetailSerializer()

    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'confirm_password', 'profile']
        write_only_fields = ['password']
        read_only_fields = ["id"]

    @return_data
    @validate_password
    @validate_unique_email
    def validate(self, data):
        request = self.context.get('request')
        return data, request

    def create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(username=validated_data['username'], email=validated_data['email'].lower(),
                                            password=make_password(validated_data['password']))

            profile = Profile(user=user,
                              first_name=self.validated_data['profile'].get('first_name'),
                              last_name=self.validated_data['profile'].get('last_name'),
                              gender=self.validated_data['profile'].get('gender'),
                              phone=self.validated_data['profile'].get('phone'),
                              website=self.validated_data['profile'].get('website'),
                              bio=self.validated_data['profile'].get('bio'),
                              birth_day=self.validated_data['profile'].get('birth_day'),
                              profile_pic=self.validated_data['profile'].get('profile_pic'),
                              )
            profile.save()

            return user


class UserPasswordUpdate(serializers.ModelSerializer):
    old_password = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    class Meta:
        model = User
        fields = ['old_password', 'password', 'confirm_password']
        write_only_fields = ['old_password', 'password', 'confirm_password']

    @validate_password
    def validate(self, data):
        request = self.context.get('request')
        if check_password(data['old_password'], request.user.password):
            return data
        raise serializers.ValidationError("Incorrect Password")

    def update(self, instance, validated_data):
        validated_password = validated_data.get('password', instance.password)
        if validated_password:
            instance.password = make_password(validated_password)
            instance.save()
            return instance
        raise serializers.ValidationError("Something went wrong, if the problem continues please contact us")


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = None
        if '@' in data['username']:
            look_for_user = User.objects.all().filter(data['username'])
            if look_for_user.exists() and len(look_for_user) == 1:
                user = authenticate({'username': look_for_user.first().email, 'password': data['password']})
        else:
            user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


class UserDetailSerializer(serializers.ModelSerializer):
    profile = ProfileDetailSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']
        read_only_fields = ["id"]


class UserProfileDetailSerializer(serializers.ModelSerializer):
    profile = ProfilePageDetailSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']
        read_only_fields = ["id"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ["id"]

    @return_data
    @validate_unique_username
    @validate_unique_email
    def validate(self, data):
        request = self.context.get('request')
        return data, request
