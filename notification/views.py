from pprint import pprint

from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from core.permissions import IsOwnerOrReadOnly, IsOwnerOnly
from notification.models import Follower, Notification
from notification.pagination import FollowerPageNumberPagination, NotificationPageNumberPagination
from notification.serializers import FollowerDetailsSerializer, NotificationDetailSerializer


class FollowerViewSet(viewsets.ModelViewSet):
    queryset = Follower.objects.all()
    serializer_class = FollowerDetailsSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = FollowerPageNumberPagination

    def create(self, request, *args, **kwargs):
        # Check if Follower already exist
        follower_exists = Follower.objects.all().filter(observer=request.user.id,
                                                        content_type=request.data.get('content_type'),
                                                        object_id=request.data.get('object_id'))
        if follower_exists.exists():
            return Response(status=status.HTTP_409_CONFLICT)

        serializer = self.get_serializer(data={
            'content_type': self.request.data.get('content_type', 11),
            'object_id': self.request.data.get('object_id')})

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(observer=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.queryset.filter(
            observer=self.request.user,
            content_type=ContentType.objects.get_for_id(request.data.get('content_type', 11), ),
            object_id=self.request.data.get('object_id')).first()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['delete'])
    def stop_follow(self, request, *args, **kwargs):
        instance = self.queryset.filter(
            observer=self.request.user,
            content_type=ContentType.objects.get_for_id(request.data.get('content_type', 11), ),
            object_id=self.request.data.get('object_id')).first()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['delete'])
    def remove_follower(self, request, *args, **kwargs):
        instance = self.queryset.filter(
            observer=self.request.data.get('object_id'),
            content_type=ContentType.objects.get_for_id(request.data.get('content_type', 11)),
            object_id=self.request.user.id).first()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationDetailSerializer
    permission_classes = [IsOwnerOnly]
    pagination_class = NotificationPageNumberPagination
    http_method_names = ['get', 'patch', 'delete', 'head', 'options']

    def list(self, request, *args, **kwargs):
        notifications = self.queryset.filter(observers=request.user).exclude(sender=request.user)
        print(len(notifications))
        if notifications.exists():
            return Response(self.serializer_class(notifications, many=True).data)
        return Response(status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, *args, **kwargs):
        instance = get_object_or_404(self.queryset, pk=kwargs.get('pk'))
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(self.serializer_class(instance).data, status=status.HTTP_206_PARTIAL_CONTENT)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.seen = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
