from functools import wraps

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.response import Response


def paginate_action(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        queryset, class_serializer, request = func(self, *args, **kwargs)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = class_serializer(page, context={'request': request}, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = class_serializer(queryset, many=True)
        return Response(serializer.data)

    return inner


def validate_unique_email(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        data, request = func(self, *args, **kwargs)
        email = data.get('email').lower()
        existing = User.objects.filter(email=email).first()
        if existing and not existing == request.user:
            raise serializers.ValidationError("This e-mail has already registered")
        return data, request

    return inner


def validate_unique_username(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        data, request = func(self, *args, **kwargs)
        username = data.get('username').lower()
        existing = User.objects.filter(username=username).first()
        if existing and not existing == request.user:
            raise serializers.ValidationError("This name has already registered")
        return data, request

    return inner


def return_data(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        data, request = func(self, *args, **kwargs)
        return data

    return inner


def validate_password(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        data, request = func(self, *args, **kwargs)
        # if isinstance(data, tuple):
        #     data = data[0]
        #     re
        if not data.get('password') or not data.get('confirm_password'):
            raise serializers.ValidationError("Please enter a password and confirm it.")
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Those passwords don't match.")
        return data, request

    return inner
