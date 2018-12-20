from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('', ShopViewSet, base_name='shop')

urlpatterns = router.urls
