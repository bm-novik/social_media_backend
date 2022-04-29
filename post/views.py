# From rest_framework
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated

# From Project
from rest_framework.response import Response

from account.models import Profile
from core.permissions import IsOwnerOrReadOnly, ImagePostIsOwnerOrReadOnly
from core.utils import paginate_action
from post.models import ImagePost
from post.pagination import PostPageNumberPagination
from post.serializers import ImagePostDetailsSerializer, ImagePostListSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = ImagePostDetailsSerializer
    pagination_class = PostPageNumberPagination
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ['get', 'post', 'head', 'options', 'delete']

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ('get', 'retrieve', 'list'):
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [ImagePostIsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return ImagePost.objects.all().prefetch_related('author', 'likes', 'comments', 'author__profile')

    @paginate_action
    def list(self, request, *args, **kwargs):
        following = Profile.objects.follow_them(user=get_object_or_404(User, pk=request.user.id))
        feed = User.objects.all().filter(id__in=following.values_list('user_id', flat=True))
        posts = ImagePost.objects.post_by_user(user_list=feed)
        return posts, ImagePostDetailsSerializer, request

    @paginate_action
    @action(detail=False)
    def explore_post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.user.id)
        posts = ImagePost.objects.post_by_user(user_list=Profile.objects.explore(user))
        return posts, ImagePostListSerializer, request

    @paginate_action
    @action(detail=True)
    def user_post(self, request, pk, *args, **kwargs):
        posts = ImagePost.objects.post_by_user(pk=pk)
        return posts, ImagePostListSerializer, request

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
