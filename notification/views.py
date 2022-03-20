from rest_framework import viewsets, status, permissions
from rest_framework.response import Response

from core.permissions import IsOwnerOrReadOnly
from notification.models import Follower
from notification.pagination import FollowerPageNumberPagination
from notification.serializers import followerDetailsSerializer


class FollowerViewSet(viewsets.ModelViewSet):
    queryset = Follower.objects.all()
    serializer_class = followerDetailsSerializer
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


