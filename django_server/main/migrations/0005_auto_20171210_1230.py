# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-10 12:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20171209_1757'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='calories',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='receipt',
            name='fat',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='receipt',
            name='protein',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='receipt',
            name='sodium',
            field=models.IntegerField(default=0),
        ),
    ]