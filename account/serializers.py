from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework import serializers

from account.models import Profile


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'first_name', 'last_name', 'city', 'bio',
                  'country', 'birth_day', 'profile_pic', 'cover_pic']
        read_only_fields = ["id"]


class ProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", 'first_name', 'last_name', 'profile_pic']
        read_only_fields = ["id"]


class RegisterSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'confirm_password', 'profile')
        write_only_fields = ['password']

    def validate_email(self, email):
        data = self.get_initial()
        existing = User.objects.filter(email=email).first()
        if existing:
            raise serializers.ValidationError("This e-mail has already registered")
        return email

    def validate(self, data):
        if not data.get('password') or not data.get('confirm_password'):
            raise serializers.ValidationError("Please enter a password and confirm it.")
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Those passwords don't match.")
        return data

    def create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(username=validated_data['username'], email=validated_data['email'],
                                            password=make_password(validated_data['password']))

            profile = Profile(user=user,
                              first_name=self.validated_data['profile'].get('first_name'),
                              last_name=self.validated_data['profile'].get('last_name'),
                              city=self.validated_data['profile'].get('city'),
                              country=self.validated_data['profile'].get('country'),
                              bio=self.validated_data['profile'].get('bio'),
                              birth_day=self.validated_data['profile'].get('birth_day'),
                              profile_pic=self.validated_data['profile'].get('profile_pic'),
                              cover_pic=self.validated_data['profile'].get('cover_pic'),
                              )
            profile.save()

            return user


class UserDetailSerializer(serializers.ModelSerializer):
    profile = ProfileDetailSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'profile']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

    def validate(self, data):
        # Making sure the username always matches the email
        email = data.get('email', None)
        if email:
            data['username'] = email
        return data














