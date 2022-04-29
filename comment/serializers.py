from django.contrib.contenttypes.models import ContentType

from account.serializers import UserDetailSerializer
from like.models import Like
from .models import Comment
from mptt.forms import TreeNodeChoiceField
from rest_framework import serializers


class CommentCreateSerializer(serializers.ModelSerializer):
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())

    class Meta:
        model = Comment
        exclude = ['user', 'is_active', 'like_count']

    def create(self, validated_data):
        Comment.objects.rebuild()
        return Comment.objects.create(**validated_data)


class CommentDetailSerializer(serializers.ModelSerializer):
    last_comment = serializers.SerializerMethodField()
    is_parent = serializers.SerializerMethodField()
    content_type = serializers.SerializerMethodField()
    did_like = serializers.SerializerMethodField()
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Comment
        exclude = ['is_active', "lft", "rght", "tree_id", "level", "updated_at"]

    @staticmethod
    def get_content_type(obj):
        return ContentType.objects.get_for_model(obj).id

    @staticmethod
    def get_last_comment(obj):
        return obj.is_leaf_node()

    @staticmethod
    def get_is_parent(obj):
        return obj.parent is None

    def get_did_like(self, obj):
        request = self.context.get('request')
        if request:
            return Like.objects.is_liked(obj, request.user)
        return None


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']


