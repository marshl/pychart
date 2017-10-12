from django.db import models
from django.utils import timezone


class Repository(models.Model):
    title = models.CharField(max_length=150)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Commit(models.Model):
    repo = models.ForeignKey(Repository)
    author = models.CharField(max_length=150)
    message = models.TextField()
    hex_sha = models.CharField(max_length=40)
    bin_sha = models.BinaryField(max_length=20)

    authored_datetime = models.DateTimeField()
    committed_datetime = models.DateTimeField()

    count = models.IntegerField()

    line_additions = models.IntegerField()
    line_subtractions = models.IntegerField()

    def __str__(self):
        return self.hex_sha
