from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Q
from django.utils import timezone

from like.models import Like
from comment.models import Comment
from notification.Mixin import SubscribeMixin
from notification.models import Follower


def user_directory_path(instance, filename):
    return 'posts/%Y/%m/%d/'.format(instance.id, filename)


class PostQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def search(self, query):
        lookups = (Q(content__icontains=query))
        print(self.filter(lookups))
        return self.filter(lookups).distinct()


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def search(self, query):
        return self.all().search(query)


class ImagePost(models.Model, SubscribeMixin):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    followers = GenericRelation(Follower, related_query_name='ImagePost')
    # slug = models.SlugField(max_length=250, unique_for_date='publish')
    image = models.ImageField(upload_to='posts', default='posts/default.jpg')
    content = models.TextField()

    likes = GenericRelation(Like, related_query_name='ImagePost')
    like_count = models.IntegerField(default=0)
    comments = GenericRelation(Like, related_query_name='ImagePost')
    comment_count = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PostManager()

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.content
