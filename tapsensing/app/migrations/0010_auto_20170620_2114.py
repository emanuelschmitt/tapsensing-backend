# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-20 21:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_session_device_model'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='session',
            unique_together=set([]),
        ),
    ]