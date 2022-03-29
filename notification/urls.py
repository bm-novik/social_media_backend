from rest_framework import routers
from notification.views import FollowerViewSet, NotificationViewSet

app_name = 'follower'
router = routers.DefaultRouter()

router.register(prefix='follower', viewset=FollowerViewSet, basename='follower')
router.register(prefix='notifications', viewset=NotificationViewSet, basename='notifications')

urlpatterns = router.urls
