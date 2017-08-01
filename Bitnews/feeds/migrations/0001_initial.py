# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-30 12:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feeds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Feeds',
            },
        ),
        migrations.CreateModel(
            name='NewsItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('link', models.CharField(max_length=200)),
                ('pub_date', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'New Items',
            },
        ),
        migrations.CreateModel(
            name='ProductItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('link', models.CharField(max_length=200)),
                ('pub_date', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Products Items',
            },
        ),
        migrations.AddField(
            model_name='feeds',
            name='news_items',
            field=models.ManyToManyField(blank=True, to='feeds.NewsItems'),
        ),
        migrations.AddField(
            model_name='feeds',
            name='product_item',
            field=models.ManyToManyField(blank=True, to='feeds.ProductItems'),
        ),
        migrations.AddField(
            model_name='feeds',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.UserProfile'),
        ),
    ]
