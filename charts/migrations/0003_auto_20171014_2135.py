# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-14 10:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0002_auto_20171012_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commit',
            name='authored_datetime',
            field=models.DateTimeField(null=True),
        ),
    ]
