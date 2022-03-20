from .models import Comment
from mptt.forms import TreeNodeChoiceField
from rest_framework import serializers


class CommentCreateSerializer(serializers.ModelSerializer):
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())

    class Meta:
        model = Comment
        # fields = ('__all__')
        exclude = ['user', 'is_active', 'like_count']

    def create(self, validated_data):
        Comment.objects.rebuild()
        return Comment.objects.create(**validated_data)


class CommentDetailSerializer(serializers.ModelSerializer):
    last_comment = serializers.SerializerMethodField()
    is_parent = serializers.SerializerMethodField()

    # children = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        exclude = ['is_active', 'like_count', "lft", "rght", "tree_id", "level", "parent", "date_created", "updated_at"]

    def get_last_comment(self, obj):
        return obj.is_leaf_node()

    def get_is_parent(self, obj):
        return obj.parent is None

    # def get_children(self, obj):
    #     return obj.get_children().filter(is_active=True)


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']


