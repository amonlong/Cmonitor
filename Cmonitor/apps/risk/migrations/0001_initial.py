# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-16 11:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RiskOverDueRate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('delayRate0', models.FloatField(default=0.0)),
                ('delayRate3', models.FloatField(default=0.0)),
                ('delayRate7', models.FloatField(default=0.0)),
                ('delayRate14', models.FloatField(default=0.0)),
                ('delayRate21', models.FloatField(default=0.0)),
                ('delayRateM1', models.FloatField(default=0.0)),
                ('delayRateM2', models.FloatField(default=0.0)),
                ('delayRateM3', models.FloatField(default=0.0)),
                ('createDate', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ('createDate',),
            },
        ),
        migrations.CreateModel(
            name='RiskPassRate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('applyNum', models.IntegerField(default=0)),
                ('passNum', models.IntegerField(default=0)),
                ('passRate', models.FloatField(default=0.0)),
                ('createDate', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ('createDate',),
            },
        ),
    ]
