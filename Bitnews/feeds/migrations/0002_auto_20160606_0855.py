# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-06 08:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NewsItems',
            new_name='NewsFeedItems',
        ),
    ]
