# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-16 13:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('risk', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='riskoverduerate',
            name='termDate',
            field=models.DateField(default=None),
        ),
    ]
