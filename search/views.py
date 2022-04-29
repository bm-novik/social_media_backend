from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny

from rest_framework.response import Response

from account.models import Profile
from account.serializers import ProfileDetailSerializer
from core.permissions import IsOwnerOrReadOnly
from post.models import ImagePost
from post.serializers import ImagePostDetailsSerializer
from search.pagination import searchPageNumberPagination


class SearchViewSet(viewsets.ViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    # permission_classes = [AllowAny]
    pagination_class = searchPageNumberPagination
    http_method_names = ['get', 'head', 'options']

    def list(self, request):
        query = request.GET.get('q', None)
        model = request.GET.get('model', None)
        data = {}

        if query is not None:
            if model in ['profile', None]:
                data["profile"] = ProfileDetailSerializer(Profile.objects.search(query), many=True).data

            if model in ['post', None]:
                data["post"] = ImagePostDetailsSerializer(ImagePost.objects.search(query), many=True).data

            return Response(data=data)
        return Response(status.HTTP_200_OK)  # just an empty queryset as default
