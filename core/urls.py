from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),


    path('', include('like.urls', namespace='like')),
    path('', include('notification.urls', namespace='follower')),
    path('', include('post.urls', namespace='post')),
    path('', include('comment.urls', namespace='comment')),
    path('', include('search.urls', namespace='search')),
    path('', include('account.urls', namespace='account')),  # Must be last!!!

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
