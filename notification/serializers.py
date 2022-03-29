
from rest_framework.serializers import ModelSerializer


from notification.models import Follower, Notification


class FollowerDetailsSerializer(ModelSerializer):
    class Meta:
        model = Follower
        fields = ('observer', 'content_type', 'object_id')
        read_only_fields = ['observer']


class NotificationCreateSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = ('observers', 'content_type', 'object_id')


class NotificationDetailSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = ('content_type', 'object_id', 'contact_object')