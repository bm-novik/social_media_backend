from rest_framework import viewsets, status
from rest_framework.response import Response

from core.permissions import IsOwnerOrReadOnly, NotificationIsOwnerOnly
from notification.models import Follower, Notification
from notification.pagination import FollowerPageNumberPagination, NotificationPageNumberPagination
from notification.serializers import FollowerDetailsSerializer, NotificationDetailSerializer


class FollowerViewSet(viewsets.ModelViewSet):
    queryset = Follower.objects.all()
    serializer_class = FollowerDetailsSerializer
    permission_classes = [IsOwnerOrReadOnly]
    # permission_classes = [permissions.AllowAny]
    pagination_class = FollowerPageNumberPagination

    def perform_create(self, serializer):
        serializer.save(observer=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.seen()
    serializer_class = NotificationDetailSerializer
    permission_classes = [NotificationIsOwnerOnly]
    pagination_class = NotificationPageNumberPagination

    def list(self, request, *args, **kwargs):
        qs = self.queryset.filter(observers=request.user).prefetch_related('User', 'ImagePost')
        print(qs)
        res = self.serializer_class(qs, many=True).data
        print(res)
        return Response(res)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.seen = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)