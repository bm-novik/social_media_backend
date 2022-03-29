from abc import ABC

from notification.models import Follower
from notification.tasks import celery_notification


class SubscribeMixin():

    def subscribe(self, instance, user=None):
        observer = instance.user if user is None else user
        """Add observer who subscribed to the chat room"""
        qs = Follower.objects.filter(observer=observer,
                                     content_type=instance.content_type,
                                     object_id=instance.object_id)
        if not qs.exists():
            Follower(observer=observer,
                     content_type=instance.content_type,
                     object_id=instance.object_id
                     ).save()

    def unsubscribe(self, instance, user=None):
        observer = instance.user if user is None else user
        """Remove the observer from the observer list"""
        follower = Follower.objects.filter(observer=observer,
                                           content_type=instance.content_type,
                                           object_id=instance.object_id)

        if follower.exists() and follower.count() == 1:
            follower.first().delete()

    def notify(self, instance):
        """Alert the observers"""
        followers = Follower.objects.filter(content_type=instance.content_type,
                                           object_id=instance.object_id)

        celery_notification(followers, instance)


class SubscribeParentMixin(SubscribeMixin):

    def subscribe(self, instance, user=None):

        """Add observer who subscribed to the chat room"""
        follower = Follower.objects.filter(observer=instance.user,
                                           content_type=instance.content_object.content_type,
                                           object_id=instance.content_object.object_id)
        if not follower.exists():
            Follower(observer=instance.user,
                     content_type=instance.content_object.content_type,
                     object_id=instance.content_object.object_id
                     ).save()

    def notify(self, instance):
        """Alert the observers"""
        followers = self.objects.all().exclude(instance)
        celery_notification(followers=followers, instance=instance)


