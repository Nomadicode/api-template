import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Shop(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=256)
	slug = models.SlugField(null=True, blank=True)
	url = models.CharField(max_length=256, null=True, blank=True)
	logo = models.ImageField(upload_to="logos", null=True, blank=True)


class Product(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=144)
	slug = models.SlugField(null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	upc = models.CharField(max_length=100, null=True, blank=True)
	base_price = models.FloatField(default=0.0)


class Inventory(models.Model):
	shop = models.ForeignKey(Shop, related_name='inventory', on_delete=models.CASCADE)
	product = models.ForeignKey(Product, related_name='inventory', on_delete=models.CASCADE)
	price = models.FloatField(default=0.0)
	quantity = models.IntegerField(default=0)
