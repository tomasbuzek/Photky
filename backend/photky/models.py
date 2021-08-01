from django.db import models
from django.contrib.auth.models import AbstractUser

from django.conf import settings

# Create your models here.

class User(AbstractUser):
    pass


class Photo(models.Model):
    image = models.ImageField()
    filename = models.CharField(max_length=256)
    added = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.filename
