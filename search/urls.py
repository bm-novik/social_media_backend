# From rest_framework
from rest_framework import routers

# From project
from search.views import SearchViewSet

app_name = 'search'
router = routers.DefaultRouter()

router.register(prefix='search', viewset=SearchViewSet, basename='search')

urlpatterns = router.urls
