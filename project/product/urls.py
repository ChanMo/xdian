from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('', ProductViewSet, base_name='product')
urlpatterns = router.urls
