# From rest_framework
from rest_framework import routers

# From project
from feed.views import FeedHomeViewSet

app_name = 'feed'
router = routers.DefaultRouter()

router.register(prefix='home', viewset=FeedHomeViewSet, basename='home')

urlpatterns = router.urls
