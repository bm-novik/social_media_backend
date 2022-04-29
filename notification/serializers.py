from rest_framework.relations import RelatedField
from rest_framework.serializers import ModelSerializer

from notification.models import Follower, Notification
from like.models import Like
from comment.models import Comment
from post.models import ImagePost
from account.models import Profile
from account.serializers import ProfileDetailSerializer, UserDetailSerializer
from comment.serializers import CommentDetailSerializer
from like.serializers import LikeDetailsSerializer
from post.serializers import ImagePostDetailsSerializer, ImageNotificationDetailsSerializer


class NotificationRelatedField(RelatedField):

    def to_internal_value(self, data):
        """
        Transform the *incoming* primitive data into a native value.
        """
        raise NotImplementedError(
            '{cls}.to_internal_value() must be implemented for field '
            '{field_name}. If you do not need to support write operations '
            'you probably want to subclass `ReadOnlyField` instead.'.format(
                cls=self.__class__.__name__,
                field_name=self.field_name,
            )
        )

    # Serialize tagged objects to a simple textual representation.
    def to_representation(self, obj):
        if isinstance(obj, ImagePost):
            serializer = ImagePostDetailsSerializer(obj)
        elif isinstance(obj, Follower):
            serializer = FollowerDetailsSerializer(obj)
        elif isinstance(obj, Profile):
            serializer = ProfileDetailSerializer(obj)
        elif isinstance(obj, Like):
            serializer = LikeDetailsSerializer(obj)
        elif isinstance(obj, Comment):
            serializer = CommentDetailSerializer(obj)
        else:
            raise Exception('Unexpected type of tagged object')

        return serializer.data


class FollowerDetailsSerializer(ModelSerializer):
    class Meta:
        model = Follower
        fields = ('observer', 'content_type', 'object_id')
        read_only_fields = ['observer']


class NotificationCreateSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = ('observers', 'content_type', 'object_id', 'sender')


class NotificationDetailSerializer(ModelSerializer):
    contact_object = NotificationRelatedField(read_only=True)
    sender = UserDetailSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'seen', 'contact_object', 'content_type', 'object_id', 'sender', 'notification_massage']
        read_only_fields = ['id', 'contact_object', 'content_type', 'object_id', 'sender', 'notification_massage']
        depth = 1

    def update(self, instance, validated_data):
        instance.seen = validated_data.get('seen', instance.seen)
        instance.save()
        return instance



