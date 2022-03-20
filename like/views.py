from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from core.permissions import IsOwnerOrReadOnly
from .filters import LikeFilter
from .models import Like
from .pagination import LikePageNumberPagination
from .serializers import LikeSerializer, LikeCreateSerializer


# Lead ViewSet
class LikeViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.AllowAny]
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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.value = 0
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
