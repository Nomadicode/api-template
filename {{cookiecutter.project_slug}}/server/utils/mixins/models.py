import uuid

from django.db import models
from django.utils import timezone


class UUIDMixin(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

	class Meta:
		abstract = True


class TimestampMixin(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(null=True, blank=True)

	class Meta:
		abstract = True

	def save(self, *args, **kwargs):
		self.updated_at = timezone.now()
	
		super(TimestampMixin, self).save(*args, **kwargs)
