# Generated by Django 2.1.5 on 2019-02-28 17:55

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('track', '0003_auto_20190226_1333'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Profile',
            new_name='Settings',
        ),
    ]
