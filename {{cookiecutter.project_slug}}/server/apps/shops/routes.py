from django.urls import path, include

from apps.shops.views import InventoryViewSet, \
                             ProductViewSet, \
                             ShopViewSet

from rest_framework.routers import SimpleRouter

APP_PREFIX = ''

router = SimpleRouter()
router.register(r'shops', ShopViewSet)
router.register(r'inventory', InventoryViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path(r'', include(router.urls))
]
