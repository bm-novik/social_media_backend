from rest_framework.serializers import ModelSerializer
from account.serializers import UserDetailSerializer
from like.serializers import LikeSerializer

from post.models import ImagePost


class ImagePostSerializer(ModelSerializer):
    author = UserDetailSerializer(read_only=True)
    like = LikeSerializer(many=True, read_only=True)
    # comments

    class Meta:
        model = ImagePost
        fields = ['id', 'image', "content", "like_count", "comment_count", "author", 'like']
        read_only_fields = ['id',  "like_count", "comment_count", "author", 'like']


