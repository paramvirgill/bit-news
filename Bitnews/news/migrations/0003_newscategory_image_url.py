# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-31 07:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20160530_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='newscategory',
            name='image_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]