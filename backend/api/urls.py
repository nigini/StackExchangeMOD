from api.views import TagViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'tags', TagViewSet, base_name='tag')
urlpatterns = router.urls