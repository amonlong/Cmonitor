# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-17 14:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productfirm',
            name='title',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
    ]
