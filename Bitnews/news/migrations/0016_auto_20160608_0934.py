# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-08 09:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0015_auto_20160608_0832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='image_url',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
