import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

	def __str__(self):
		return self.email

	@property
	def name(self):
		return f"{self.first_name} {self.last_name}"
