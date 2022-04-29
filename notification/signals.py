from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models import Profile
from notification.models import Follower
from notification.tasks import celery_notification


@receiver(post_save, sender=Follower)
def follow_post_save(sender, instance, created, *args, **kwargs):
    ct = ContentType.objects.get_for_model(Profile)
    ict = instance.content_type
    if instance.is_active and ict == ct:
        celery_notification(followers=[instance], instance=instance)
