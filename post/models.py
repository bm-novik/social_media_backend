from datetime import date

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Q

from like.models import Like
from comment.models import Comment
from notification.Mixin import SubscribeMixin
from notification.models import Follower, Notification


def post_directory_path(instance, filename):
    return f'posts/{instance.author.profile.first_name}_{instance.author.profile.last_name}/{date.today()}/{filename}'


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

    def post_by_user(self, pk=None, user_list=None):
        if pk is not None:
            return self.all().filter(author_id=pk)
        if user_list is not None:
            return self.all().filter(author_id__in=user_list.values_list('id', flat=True))


class ImagePost(models.Model, SubscribeMixin):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')

    image = models.ImageField(upload_to=post_directory_path, default='posts/default.jpg')
    content = models.TextField()

    likes = GenericRelation(Like, related_query_name='ImagePost')
    like_count = models.IntegerField(default=0)
    comments = GenericRelation(Like, related_query_name='ImagePost')
    comment_count = models.IntegerField(default=0)
    notification = GenericRelation(Notification, related_query_name='ImagePost')
    followers = GenericRelation(Follower, related_query_name='ImagePost')

    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PostManager()

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.content
