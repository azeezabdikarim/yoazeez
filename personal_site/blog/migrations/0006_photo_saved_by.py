# Generated by Django 3.1.3 on 2020-11-30 05:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0005_photo_total_votes'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='saved_by',
            field=models.ManyToManyField(related_name='saves', to=settings.AUTH_USER_MODEL),
        ),
    ]
