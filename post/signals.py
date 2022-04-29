from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.contenttypes.models import ContentType

from notification.models import Follower
from post.models import ImagePost


@receiver(post_save, sender=ImagePost)
def image_post_post_save(sender, instance, created, *args, **kwargs):
    if created:
        Follower(observer=instance.author,
                 content_type=ContentType.objects.get_for_model(ImagePost),
                 object_id=instance.id).save()
