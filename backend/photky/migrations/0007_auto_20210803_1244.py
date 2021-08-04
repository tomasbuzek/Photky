# Generated by Django 3.2.5 on 2021-08-03 10:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photky', '0006_alter_photo_filename'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='content_type',
            field=models.CharField(default='image/jpeg', editable=False, max_length=64),
        ),
        migrations.AlterField(
            model_name='photo',
            name='filename',
            field=models.CharField(blank=True, editable=False, max_length=256),
        ),
        migrations.AlterField(
            model_name='photo',
            name='owner',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='photo',
            name='thumbnail',
            field=models.ImageField(blank=True, default=None, editable=False, null=True, upload_to='thumbnails'),
        ),
    ]