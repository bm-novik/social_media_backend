from rest_framework.serializers import ModelSerializer

from account.serializers import UserSerializer
from like.models import Like


class LikeSerializer(ModelSerializer):

    class Meta:
        model = Like
        exclude = ["is_active", "date_created", "updated_at"]


class LikeDetailsSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ('user', 'value', 'updated')


class LikeCreateSerializer(ModelSerializer):

    class Meta:
        model = Like
        exclude = ["user", "value", "is_active", "date_created", "updated_at"]
