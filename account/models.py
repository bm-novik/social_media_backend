# From Django
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.core import validators
from django.db import models


# From 3rd party

# From Project
from PIL import Image
from django.db.models import Q

from notification.Mixin import SubscribeMixin, NotifierMixin
from notification.models import Follower


class CommonInfo(models.Model):
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Country(CommonInfo):
    name = models.CharField(max_length=128, null=False, blank=False)

    def __str__(self):
        return self.name


class City(CommonInfo):
    name = models.CharField(max_length=128, null=False, blank=False)
    models.ForeignKey(Country, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class Address(CommonInfo):
    address = models.CharField(max_length=128, null=False, blank=False)
    models.ForeignKey(City, on_delete=models.RESTRICT)

    def __str__(self):
        return self.address


class ProfileQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def search(self, query):
        lookups = (Q(first_name__icontains=query) |
                   Q(last_name__icontains=query) |
                   Q(city__name__icontains=query) |
                   Q(country__name__icontains=query)
                   )
        return self.filter(lookups).distinct()


class ProfileManager(models.Manager):
    def get_queryset(self):
        return ProfileQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def follow_me(self, user):
        qs = Follower.objects.all().filter(profile=user.profile, is_active=True)
        return self.filter(followers__in=qs)

    def follow_them(self, user):
        qs = Follower.objects.all().filter(observer=user, is_active=True, content_type=11)
        return self.filter(id__in=qs.values_list('object_id', flat=True))

    def search(self, query):
        return self.all().search(query)


class Profile(CommonInfo, SubscribeMixin):
    # Foreign relations
    user = models.OneToOneField(User, on_delete=models.RESTRICT, related_name='profile')
    followers = GenericRelation(Follower, related_query_name='profile', blank=True)
    city = models.ForeignKey(City, on_delete=models.RESTRICT, related_name='city')
    country = models.ForeignKey(Country, on_delete=models.RESTRICT, related_name='country')
    # notify_methods = models.ManyToManyField(notify_methods, on_delete=models.RESTRICT, related_name='notify_methods')

    # Personal Bio
    first_name = models.CharField(max_length=128, null=False, blank=False)
    last_name = models.CharField(max_length=128, null=False, blank=False)
    birth_day = models.DateField(blank=True, null=True, default=None)
    bio = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(blank=True, null=True, default='default.jpg', upload_to='profile_pics')
    cover_pic = models.ImageField(blank=True, null=True, default='default.jpg', upload_to='cover_pic')

    objects = ProfileManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self):
        super().save()
        try:
            img = Image.open(self.profile_pic.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.profile_pic.path)

        except ValueError:
            pass
