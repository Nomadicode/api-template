
import http
from django.db.models import Q

from rest_framework import viewsets
from rest_framework.response import Response

from django.utils.translation import get_language_from_request


class NoPatchViewSet(viewsets.ModelViewSet):
	def partial_update(self, request, *args, **kwargs):
		return Response(status=http.HTTPStatus.METHOD_NOT_ALLOWED)

	def update(self, request, *args, **kwargs):
		kwargs['partial'] = True

		return super().update(request, *args, **kwargs)


class PreCommitViewSet(viewsets.ModelViewSet):
	def pre_update(self, request, *args, **kwargs):
		pass

	def update(self, request, *args, **kwargs):
		kwargs['partial'] = True
		self.pre_update(request, *args, **kwargs)

		return super().update(request, *args, **kwargs)

	def pre_create(self, request, *args, **kwargs):
		pass

	def create(self, request, *args, **kwargs):
		self.pre_create(request, *args, **kwargs)
		return super().create(request, *args, **kwargs)


class NoPostViewSet(NoPatchViewSet, viewsets.ModelViewSet):
	def create(self, request, *args, **kwargs):
		return Response(status=http.HTTPStatus.METHOD_NOT_ALLOWED)


class NestedParentViewMixin():
	parent_lookups = {
#		"parent_lookup_field": (<parent_field_on_object>, <parent_object_lookup_field>, <lookup_modifiers (iexact, icontains)>)
	}

	def get_queryset(self):
		base_queryset = super().get_queryset()

		parent_keys = self.parent_lookups.keys()
		provided_keys = self.kwargs.keys()

		for lookup in provided_keys:
			if lookup in parent_keys:
				parent_field = "__".join(self.parent_lookups[lookup])

				base_queryset = base_queryset.filter(**{
					parent_field: self.kwargs[lookup]
				})

		return base_queryset
