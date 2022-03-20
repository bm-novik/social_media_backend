from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from django.db import models

class likeQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def class_name(self):
        return(Like)


class likeManager(models.Manager):
    def get_queryset(self):
        return likeQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def class_name(self):
        return "Like"


class Like(models.Model):
    class LikeChoices(models.IntegerChoices):
        LIKE = 1
        __empty__ = 'Rate this'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(default=1, choices=LikeChoices.choices)

    date_created = models.DateField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    is_active = models.BooleanField(default=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    objects = likeManager()

    def __str__(self):
        return f'Like on {self.content_object}, By - {self.user.profile.first_name} '
