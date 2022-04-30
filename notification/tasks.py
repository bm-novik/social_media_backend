from __future__ import absolute_import, unicode_literals
import json
from celery import shared_task

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from rest_framework.generics import get_object_or_404

from .email import send_notification_email
from .models import Notification


@shared_task
def send_email_task(data):
    data = json.loads(data)
    return send_notification_email(name=data.get('name'),
                                   email=data.get('email'),
                                   notification=data['notification'].get('notification_massage')
                                   )


@shared_task
def create_notification_task(data):
    data = json.loads(data)
    Notification(observers=get_object_or_404(User, pk=data['notification'].get('observers')),
                 content_type=ContentType.objects.get_for_id(data['notification']['content_type']),
                 object_id=data['notification'].get('object_id'),
                 sender=get_object_or_404(User, pk=data['notification'].get('sender'))
                 ).save()


def convert_to_dict(follower, instance):
    data = {}
    if instance.__class__.__name__ in ('Like', 'ImagePost', 'Comment'):
        data["notification"] = {
            "observers": int(follower.observer.id),
            "content_type": int(instance.content_type_id),
            "object_id": int(instance.object_id),
            "sender": int(instance.user.id),
        }
        if instance.__class__.__name__ == 'Like':
            data["notification"]["notification_massage"] = f' Liked {instance.user.profile.first_name} ' \
                                                           f'{instance.user.profile.last_name} post'
        if instance.__class__.__name__ == 'ImagePost':
            data["notification"][
                "notification_massage"] = f' is also interested in {instance.author.profile.first_name} '
            f'{instance.author.profile.last_name} check it out!'
        if instance.__class__.__name__ == 'Comment':
            data["notification"]["notification_massage"] = f' commented on {instance.user.profile.first_name} ' \
                                                           f'{instance.user.profile.last_name} post'

    if instance.__class__.__name__ in ('Follower', 'Profile'):
        data["notification"] = {
            "observers": int(instance.content_object.user.id),
            "content_type": int(instance.content_type_id),
            "object_id": int(instance.observer_id),
            "sender": int(instance.observer.id),
            "notification_massage": f' has started following you'
        }

    data["name"] = f'{follower.observer.profile.first_name} {follower.observer.profile.last_name}'
    data["email"] = follower.observer.email

    return data


def celery_notification(followers, instance):
    for follower in followers:
        data = convert_to_dict(follower, instance)
        data = json.dumps(data)
        create_notification_task.delay(data)
        send_email_task.delay(data)
