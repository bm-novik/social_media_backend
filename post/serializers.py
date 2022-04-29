from django.contrib.contenttypes.models import ContentType
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from account.serializers import UserDetailSerializer
from like.models import Like
from like.serializers import LikeSerializer

from post.models import ImagePost


class ImagePostDetailsSerializer(ModelSerializer):
    author = UserDetailSerializer(read_only=True)
    like = LikeSerializer(many=True, read_only=True)
    did_like = SerializerMethodField()
    content_type = SerializerMethodField()

    # comments

    class Meta:
        model = ImagePost
        fields = ['id', 'content_type', 'image', "content", 'did_like', "like_count", "comment_count", "author", 'like', 'date_created']
        read_only_fields = ['id', "like_count", "comment_count", "author", 'like']

    def get_did_like(self, obj):
        request = self.context.get('request')
        if request:
            return Like.objects.is_liked(obj, request.user)
        return None

    @staticmethod
    def get_content_type(obj):
        return ContentType.objects.get_for_model(obj).id


class ImageNotificationDetailsSerializer(ModelSerializer):
    # comments
    class Meta:
        model = ImagePost
        fields = ['id', 'image', "content"]
        read_only_fields = ['id', "image", "content"]


class ImagePostListSerializer(ModelSerializer):
    class Meta:
        model = ImagePost
        fields = ['id', 'image', "content", "like_count", "comment_count"]
        read_only_fields = ['id', "like_count", "comment_count"]
