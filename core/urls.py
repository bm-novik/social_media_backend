from django.contrib import admin
from django.urls import path, include

import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),


    path('', include('feed.urls', namespace='feed')),
    path('', include('like.urls', namespace='like')),
    path('', include('notification.urls', namespace='follower')),
    path('', include('post.urls', namespace='post')),
    path('', include('comment.urls', namespace='comment')),
    path('', include('search.urls', namespace='search')),

    path('', include('account.urls', namespace='account')),  # Must be last!!!

    path('__debug__/', include('debug_toolbar.urls')),
]

