from io import BytesIO
from PIL import Image, ImageOps

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile

from django.conf import settings

# Create your models here.

class User(AbstractUser):
    pass


THUMBNAIL_CONTENT_TYPE = "image/jpeg"

class Photo(models.Model):
    image = models.ImageField(upload_to='photos')
    content_type = models.CharField(max_length=64, default=THUMBNAIL_CONTENT_TYPE, editable=False)
    thumbnail = models.ImageField(upload_to='thumbnails', default=None, null=True, blank=True, editable=False)
    filename = models.CharField(max_length=256, blank=True, editable=False)
    added = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)

    def save(self, *args, **kwargs):
        self.content_type = self.image.file.content_type
        self.create_thumbnail()
        self.filename = self.image.name
        super(Photo, self).save(*args, **kwargs)

    def create_thumbnail(self):
        try:
            with Image.open(self.image) as im:
                thumb = ImageOps.fit(im, [256, 256], Image.ANTIALIAS).convert('RGB')
                temp_thumb = BytesIO()
                thumb.save(temp_thumb, "JPEG")
                temp_thumb.seek(0)

                self.thumbnail.save(self.image.name, ContentFile(temp_thumb.read()), save=False)
        except Exception as e:
            print(e)

    def __str__(self) -> str:
        return self.filename
