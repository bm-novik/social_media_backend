from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.db import models


class NotificationQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def is_seen(self):
        return self.filter(is_active=True, seen=False)


class NotificationManager(models.Manager):
    def get_queryset(self):
        return NotificationQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def seen(self):
        return self.all().is_seen()


class Notification(models.Model):
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    notification_massage = models.CharField(max_length=128, null=True, blank=True)
    sender = models.ForeignKey(User, related_name='notification_from', on_delete=models.CASCADE, null=True, blank=True)
    observers = models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE, null=True, blank=True)
    seen = models.BooleanField(default=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    objects = NotificationManager()

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f'{self.observers} has notification from (contact object is..) {self.content_object.__class__.__name__}'


class FollowerQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class FollowerManager(models.Manager):
    def get_queryset(self):
        return FollowerQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def follow_status(self, observer_id, object_id):
        if observer_id == object_id:
            return None
        qs = self.all().filter(is_active=True, observer_id=observer_id, content_type=11, object_id=object_id)
        if qs.exists():
            return True
        return False


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
