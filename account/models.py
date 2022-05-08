# From Django
from datetime import date

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models


# From 3rd party
from knox.models import AuthToken

# From Project
from PIL import Image
from django.db.models import Q

from notification.Mixin import SubscribeMixin
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


def profile_pic_directory_path(instance, filename):
    return f'profile_pic/{instance.author.profile.first_name}_{instance.author.profile.last_name}/{date.today()}/{filename}'


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
        qs2 = Follower.objects.all().filter(is_active=True, object_id=user.id, content_type=11)
        return self.filter(id__in=qs2.values_list('observer_id', flat=True))
        # return self.filter(followers__in=qs2)

    def follow_them(self, user):
        qs = Follower.objects.all().filter(is_active=True, observer_id=user.id, content_type=11)
        return self.filter(followers__in=qs)

    def explore(self, user):
        not_following = self.follow_them(user)
        return User.objects.all().filter(~Q(id__in=not_following.values_list('user_id', flat=True)))\
            .exclude(id=user.profile.id)

    def top_five(self, user):
        return self.explore(user)[:5]

    def search(self, query):
        return self.all().search(query)


class Profile(CommonInfo, SubscribeMixin):

    class Gender(models.IntegerChoices):
        PREFER_NOT_TO_STATE = 0
        WOMAN = 1
        MAN = 2
        NON_BINARY = 3
        I_DONT_IDENTIFY_WITH_ANY_GENDER = 4

    # Foreign relations
    user = models.OneToOneField(User, on_delete=models.RESTRICT, related_name='profile')
    followers = GenericRelation(Follower, related_query_name='profile', blank=True)

    # Personal Bio
    first_name = models.CharField(max_length=128, null=False, blank=False)
    last_name = models.CharField(max_length=128, null=False, blank=False)
    birth_day = models.DateField(blank=True, null=True, default=None)
    phone = models.CharField(max_length=128, null=True, blank=True)
    gender = models.IntegerField(choices=Gender.choices, null=False, blank=False)
    bio = models.TextField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    profile_pic = models.ImageField(blank=True, null=True, default='default.jpg', upload_to='profile_pic_directory_path')

    objects = ProfileManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

