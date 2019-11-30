# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-12 11:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Commit",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("author", models.CharField(max_length=150)),
                ("message", models.TextField()),
                ("hex_sha", models.CharField(max_length=40)),
                ("bin_sha", models.BinaryField(max_length=20)),
                ("authored_datetime", models.DateTimeField()),
                ("committed_datetime", models.DateTimeField()),
                ("count", models.IntegerField()),
                ("line_additions", models.IntegerField()),
                ("line_subtractions", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Repository",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=150)),
                (
                    "created_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
            ],
        ),
        migrations.AddField(
            model_name="commit",
            name="repo",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="charts.Repository"
            ),
        ),
    ]
