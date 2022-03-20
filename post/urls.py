from rest_framework import routers
from post.views import PostViewSet

app_name = 'post'
router = routers.DefaultRouter()

router.register(prefix='post', viewset=PostViewSet, basename='post')

urlpatterns = router.urls
