# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-23 16:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20170620_2114'),
    ]

    operations = [
        migrations.AddField(
            model_name='touchevent',
            name='grid_shape',
            field=models.CharField(default='initial', max_length=100),
            preserve_default=False,
        ),
    ]
