from rest_framework import permissions, viewsets, status

# from comment.forms import NewCommentForm
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from comment.models import Comment
from comment.pagination import CommentPageNumberPagination

from comment.serializers import CommentCreateSerializer, CommentUpdateSerializer, CommentDetailSerializer
from core.permissions import IsOwnerOrReadOnly
from core.utils import paginate_action


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = CommentPageNumberPagination
    http_method_names = ['get', 'post', 'head', 'options', 'patch', 'delete']

    def get_queryset(self):
        return Comment.objects.all().filter(is_active=True)

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'GET':
            return CommentDetailSerializer
        if self.request.method == 'PATCH':
            return CommentUpdateSerializer
        if self.request.method == 'POST':
            return CommentCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @paginate_action
    @action(detail=False)
    def parent_comments(self, request, *args, **kwargs):
        comments = Comment.objects.all().filter(is_active=True, parent=None, content_type=request.query_params['c'],
                                                object_id=request.query_params['o']).order_by("date_created")

        return comments, CommentDetailSerializer, request

    @paginate_action
    @action(detail=True)
    def children_comments(self, request, pk, *args, **kwargs):
        comments = get_object_or_404(Comment, pk=pk).get_children().order_by("date_created")
        print(comments)

        return comments, CommentDetailSerializer, request
