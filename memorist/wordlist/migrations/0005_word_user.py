# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-10 09:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wordlist', '0004_auto_20171122_1317'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]