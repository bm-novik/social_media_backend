from rest_framework.serializers import ModelSerializer

from notification.models import Follower, Notification


class followerDetailsSerializer(ModelSerializer):

    class Meta:
        model = Follower
        fields = ('observer', 'content_type', 'object_id')
        read_only_fields = ['observer']


class NotificationSerializer(ModelSerializer):

    class Meta:
        model = Notification
        fields = ('observers', 'content_type', 'object_id')
