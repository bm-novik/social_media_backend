from django.contrib import admin

from notification.models import Notification, Follower

admin.site.register(Notification)

admin.site.register(Follower)
