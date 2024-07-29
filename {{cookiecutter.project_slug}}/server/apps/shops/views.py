from rest_framework import viewsets

from utils.mixins.views import PreCommitViewSet, NoPatchViewSet

from apps.shops.models import Inventory, \
	                          Product, \
							  Shop

from apps.shops.serializers import InventorySerializer, \
                                   ProductSerializer, \
								   ShopSerializer


class InventoryViewSet(PreCommitViewSet, viewsets.ModelViewSet):
	queryset = Inventory.objects.all()
	serializer_class = InventorySerializer
	lookup_field = "shop_id"


class ProductViewSet(PreCommitViewSet, viewsets.ModelViewSet):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer


class ShopViewSet(NoPatchViewSet, viewsets.ModelViewSet):
	queryset = Shop.objects.all()
	serializer_class = ShopSerializer
	lookup_field = "slug"	
