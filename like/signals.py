from django.db import transaction
from django.db.models import Count
from django.dispatch import receiver
from django.db.models.signals import post_save

from like.models import Like


def count_likes(instance):
    return Like.objects.filter \
                    (is_active=True, content_type=instance.content_type, object_id=instance.object_id).\
                    aggregate(count=Count('id')).get('count')


@receiver(post_save, sender=Like)
def like_post_save(sender, instance, created, *args, **kwargs):

    # trigger new content_object like count calculation
    like_content_object = instance.content_object
    if instance.is_active:
        with transaction.atomic():
            like_content_object.like_count = count_likes(instance)
            like_content_object.subscribe(instance)
            like_content_object.notify(instance)
    else:
        with transaction.atomic():
            like_content_object.like_count = count_likes(instance)
            like_content_object.unsubscribe(instance)

    like_content_object.save()
