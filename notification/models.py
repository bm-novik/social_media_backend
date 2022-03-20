from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.db import models


class Notification(models.Model):
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    observers = models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE, null=True, blank=True)
    seen = models.BooleanField(default=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")


class FollowerQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class FollowerManager(models.Manager):
    def get_queryset(self):
        return FollowerQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()


class Follower(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    observer = models.ForeignKey(User, on_delete=models.RESTRICT, null=False, blank=False)

    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Subject
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    objects = FollowerManager()

    def delete(self):
        self.is_active = False
        self.save()

    def __str__(self):
        return f'{self.content_object} Followed By {self.observer}'


