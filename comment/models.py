from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth import authenticate

from mptt.models import MPTTModel, TreeForeignKey

from like.models import Like
from notification.Mixin import SubscribeParentMixin


class CommentQuerySet(models.QuerySet):
    def active(self):
        return self.filter(parent=None)


class CommentManager(models.Manager):
    def get_queryset(self):
        return CommentQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()


class Comment(MPTTModel, SubscribeParentMixin):
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')
    user = models.ForeignKey(User, related_name='author',
                             on_delete=models.CASCADE, default=None, null=False, blank=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    content = models.TextField()

    date_created = models.DateField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    is_active = models.BooleanField(default=True)

    likes = GenericRelation(Like, related_query_name='comment')
    like_count = models.IntegerField(default=0)

    my_objects = CommentManager()

    class MPTTMeta:
        order_insertion_by = ['-date_created']

    def __str__(self):
        return f'Author: {self.user.username}, Comment: {self.content}'
