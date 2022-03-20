# From rest_framework
from rest_framework import viewsets
from rest_framework.reverse import reverse as api_reverse
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# From Project
from account.serializers import UserDetailSerializer
from core.permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView

from feed.pagination import FeedPageNumberPagination
from notification.models import Follower, Notification
from notification.serializers import NotificationSerializer
from post.models import ImagePost
from post.serializers import ImagePostSerializer


class FeedHomeViewSet(viewsets.ViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    # permission_classes = [AllowAny]
    pagination_class = FeedPageNumberPagination

    def list(self, request):
        qs = Follower.objects.all().filter(observer=request.user, content_type=11).prefetch_related('content_object',
                                                                                                    'observer')
        post_queryset = ImagePost.objects.all().filter(author__in=[q.content_object.user for q in qs]).prefetch_related(
            'author')

        data = {
            "register_url": api_reverse("account:register", request=request),
            "login_url": api_reverse("account:login", request=request),
            "logout_url": api_reverse("account:logout", request=request),
            "posts": ImagePostSerializer(post_queryset, many=True).data,
            'user_details': UserDetailSerializer(request.user).data,
            "notifiations": NotificationSerializer(Notification.objects.all().filter(observers=request.user),
                                                   many=True).data}
        return Response(data)
