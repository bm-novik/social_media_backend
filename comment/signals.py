from django.db import transaction
from django.db.models import Count
from django.dispatch import receiver
from django.db.models.signals import post_save

from comment.models import Comment


def count_comments(instance):
    return Comment.objects.filter \
        (is_active=True, content_type=instance.content_type, object_id=instance.object_id). \
        aggregate(count=Count('id')).get('count')


@receiver(post_save, sender=Comment)
def comment_post_save(sender, instance, created, *args, **kwargs):
    # trigger new content_object comment count calculation
    comment_content_object = instance.content_object

    if instance.is_active:
        with transaction.atomic():
            if created:
                comment_content_object.comment_count = count_comments(instance)

                comment_content_object.subscribe(instance)
                comment_content_object.notify(instance)
    else:
        with transaction.atomic():
            comment_content_object.comment_count = count_comments(instance)

    comment_content_object.save()
