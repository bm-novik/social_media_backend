from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from core.permissions import IsOwnerOrReadOnly
from .filters import LikeFilter
from .models import Like
from .pagination import LikePageNumberPagination
from .serializers import LikeSerializer, LikeCreateSerializer


# Like ViewSet
class LikeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = LikePageNumberPagination
    queryset = Like.objects.all()
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filter_class = LikeFilter
    http_method_names = ['get', 'post', 'head', 'options', 'delete']

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'POST':
            return LikeCreateSerializer
        else:
            return LikeSerializer

    def create(self, request, *args, **kwargs):
        # Check if like already exist
        like_exists = Like.objects.all().filter(user=request.user.id,
                                                content_type=request.data.get('content_type'),
                                                object_id=request.data.get('object_id'))
        if like_exists.exists():
            return Response(status=status.HTTP_409_CONFLICT)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = Like.objects.all().filter(user=request.user.id,
                                             content_type=request.data.get('content_type'),
                                             object_id=request.data.get('object_id')).first()
        instance.value = 0
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
