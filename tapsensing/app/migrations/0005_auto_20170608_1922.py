# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-08 19:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20170608_1818'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensordata',
            name='y',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sensordata',
            name='z',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
