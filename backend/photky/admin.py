from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Photo, User

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Photo)
