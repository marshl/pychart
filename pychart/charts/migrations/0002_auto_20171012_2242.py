# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-12 11:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("charts", "0001_initial")]

    operations = [
        migrations.AlterModelOptions(
            name="repository", options={"verbose_name_plural": "repositories"}
        ),
        migrations.AddField(
            model_name="repository",
            name="path",
            field=models.CharField(default="temp", max_length=2048),
            preserve_default=False,
        ),
    ]
