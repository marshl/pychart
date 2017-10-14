from django.db import models
from django.utils import timezone

import git
import re


class Repository(models.Model):
    title = models.CharField(max_length=150)
    created_date = models.DateTimeField(default=timezone.now)

    path = models.CharField(max_length=2048)

    # branch = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "repositories"

    def get_git_repo(self):
        return git.Repo(self.path)

    def load_commits(self):
        repo = self.get_git_repo()

        for git_commit in repo.iter_commits():
            if Commit.objects.filter(hex_sha=git_commit.hexsha).exists():
                continue

            commit = Commit(self, git_commit)
            commit.save()

    def delete_commits(self):
        Commit.objects.filter(repo=self).delete()


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


class RepositoryManager(models.Manager):
    def create_repo(self, title, path):
        repo = self.create(title=title, path=path)
        repo.save()


class CommitManager(models.Manager):
    def create_commit(self, repo: git.Repo, commit: git.Commit):
        c = self.create(repo=repo)
        c.author = commit.author
        c.authored_datetime = commit.authored_datetime
        c.message = commit.message
        c.hex_sha = commit.hexsha
        c.bin_sha = commit.binsha
        c.committed_datetime = commit.committed_datetime
        c.count = commit.count()

        try:
            diffs = commit.diff(commit.hexsha, create_patch=True, ignore_blank_lines=True,
                                ignore_space_at_eol=True, diff_filter='adm')

            diff_text = '\n'.join([str(x) for x in diffs])
            c.line_additions = len(re.findall('^\+ ', diff_text, re.MULTILINE))
            c.line_subtractions = len(re.findall('^- ', diff_text, re.MULTILINE))
        except git.GitCommandError:
            pass
