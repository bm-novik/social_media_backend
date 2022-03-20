from rest_framework import routers
from notification.views import FollowerViewSet

app_name = 'follower'
router = routers.DefaultRouter()

router.register(prefix='follower', viewset=FollowerViewSet, basename='follower')

urlpatterns = router.urls
