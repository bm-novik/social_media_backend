from __future__ import absolute_import, unicode_literals

import json
from django.core.serializers import serialize

from celery import shared_task

from .email import send_notification_email
from .serializers import NotificationCreateSerializer


@shared_task
def send_email_task(follower, instance):
    return send_notification_email(f'{follower.observer.profile.first_name} {follower.observer.profile.last_name}',
                                   follower.observer.email,
                                   f'{instance.user.profile.first_name} {instance.user.profile.last_name} has '
                                   f'{instance.__class__.__name__} this {instance.content_object} post')


@shared_task
def create_notification_task(follower, instance):
    # data = json.load(data)
    serializer = NotificationCreateSerializer(
        data={"observers": follower.observer_id, "content_type": instance.content_type_id,
              "object_id": instance.object_id})
    serializer.is_valid(raise_exception=True)
    serializer.save()


def celery_notification(followers, instance):
    for follower in followers:
        create_notification_task(follower, instance)
        send_email_task(follower, instance)

        # data = serialize("json", {"follower": follower, "instance": instance})
        # create_notification_task(data)
        # send_email_task.da(data)
