from rest_framework import serializers

from apps.shops.models import Inventory, \
							  Product, \
							  Shop


class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product


class InventorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Inventory


class ShopSerializer(serializers.ModelSerializer):
	class Meta:
		model = Shop
