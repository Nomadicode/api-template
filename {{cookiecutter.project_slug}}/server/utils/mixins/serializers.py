from collections import OrderedDict
from rest_framework import serializers

from django.core.exceptions import ObjectDoesNotExist


class CreatableSlugRelatedField(serializers.SlugRelatedField):
	def to_internal_value(self, data):
		try:
			return self.get_queryset().get_or_create(**{self.slug_field: data})[0]
		except ObjectDoesNotExist:
			self.fail('does_not_exist', slug_name=self.slug_field, value=smart_str(data))
		except (TypeError, ValueError):
			self.fail('invalid')


class AsymmetricRelatedField(serializers.PrimaryKeyRelatedField):
	def __init__(self, *args, **kwargs):
		self.serializer_class = kwargs.pop('serializer_class')
		super().__init__()

	def to_representation(self, value):
		return self.serializer_class(value).data

	def get_queryset(self):
		if self.queryset:
			return self.queryset
		return self.serializer_class.Meta.model.objects.all()

	def get_choices(self, cutoff=None):
		queryset = self.get_queryset()
		if queryset is None:
			return {}

		if cutoff is not None:
			queryset = queryset[:cutoff]

		return OrderedDict([
			(
				item.pk,
				self.display_value(item)
			)
			for item in queryset
		])

	def use_pk_only_optimization(self):
		return False

	@classmethod
	def from_serializer(cls, serializer, name=None, args=(), kwargs={}):
		if name is None:
			name = f"{serializer.__class__.name}AsymetricAutoField"

		return type(name, [cls], {"serializer_class": serializer})
