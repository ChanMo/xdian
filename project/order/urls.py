from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('', OrderViewSet, base_name='order')
urlpatterns = router.urls
