from django.db import models

from django.contrib.auth import get_user_model

from utils.security import generate_reset_token

User = get_user_model()


# Create your models here.
class PasswordToken(models.Model):
    user = models.ForeignKey(User, related_name='reset_tokens', on_delete=models.CASCADE)
    token = models.CharField(max_length=128, default=generate_reset_token)
    created_at = models.DateTimeField(auto_now_add=True)
