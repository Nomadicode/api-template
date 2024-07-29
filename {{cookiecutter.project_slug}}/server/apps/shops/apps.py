from django.apps import AppConfig


class ShopsConfig(AppConfig):
	name = 'apps.shops'

	def ready(self):
		import apps.shops.signals
