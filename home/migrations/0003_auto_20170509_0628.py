# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-09 06:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20170509_0627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='uri_authorization',
            field=models.NullBooleanField(default=False),
        ),
    ]