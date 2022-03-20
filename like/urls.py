# From rest_framework
from rest_framework import routers

# From project
from like.views import LikeViewSet

app_name = 'like'
router = routers.DefaultRouter()

router.register(prefix='like', viewset=LikeViewSet, basename='like')

urlpatterns = router.urls
