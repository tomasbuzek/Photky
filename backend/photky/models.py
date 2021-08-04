from io import BytesIO
from PIL import Image, ImageOps

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
from django.db import models

THUMBNAIL_CONTENT_TYPE = "image/jpeg"


class User(AbstractUser):
    pass


class Photo(models.Model):
    """Model representing the photo instance.

    Contains:
     - image file
     - content type specification
     - thumbnail file
     - filename
     - date added
     - foreign key owner (User)
    """
    image = models.ImageField(upload_to='photos')
    content_type = models.CharField(max_length=64, default=THUMBNAIL_CONTENT_TYPE, editable=False)
    thumbnail = models.ImageField(upload_to='thumbnails', default=None, null=True, blank=True, editable=False)
    filename = models.CharField(max_length=256, blank=True, editable=False)
    added = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)

    def save(self, *args, **kwargs):
        """Save the Photo instance.

        Automatically sets the filename, content type and generates thumbnail.
        """
        self.content_type = self.image.file.content_type
        self.create_thumbnail()
        self.filename = self.image.name
        super(Photo, self).save(*args, **kwargs)

    def create_thumbnail(self):
        """Photo thumbnail generation using Pillow."""
        try:
            with Image.open(self.image) as im:
                # Fits the image to 256x256 and saves it as JPG to byte stream.
                thumb = ImageOps.fit(im, [256, 256], Image.ANTIALIAS).convert('RGB')
                temp_thumb = BytesIO()
                thumb.save(temp_thumb, "JPEG")
                temp_thumb.seek(0)
                # Set the Photo thumbnail image.
                self.thumbnail.save(self.image.name, ContentFile(temp_thumb.read()), save=False)
        except Exception as e:
            print(e)

    def __str__(self) -> str:
        return self.filename
