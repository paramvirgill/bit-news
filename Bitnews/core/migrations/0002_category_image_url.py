# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-31 07:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]