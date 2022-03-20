# From rest_framework
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

# From Project
from core.permissions import IsOwnerOrReadOnly
from post.models import ImagePost
from post.pagination import PostPageNumberPagination
from post.serializers import ImagePostSerializer


class PostViewSet(viewsets.ModelViewSet):
    # permission_classes = [AllowAny]
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ImagePostSerializer
    pagination_class = PostPageNumberPagination
    http_method_names = ['get', 'post', 'head', 'options', 'delete']

    def get_queryset(self):
        return ImagePost.objects.all().prefetch_related('author', 'likes', 'comments', 'author__profile')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
