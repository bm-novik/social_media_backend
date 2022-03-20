from rest_framework import routers
from comment.views import CommentViewSet

app_name = 'comment'
router = routers.DefaultRouter()

router.register(prefix='comment', viewset=CommentViewSet, basename='comment')

urlpatterns = router.urls
