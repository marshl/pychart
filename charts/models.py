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

    def get_repo(self):
        return git.Repo(self.path)

    def get_commits(self, repo):
        # return self.get_repo().tree().list_traverse()
        # Use active branch
        # TODO: Use user specified branch instead
        return repo.iter_commits()

    def load_commits(self):
        repo = self.get_repo()

        # head_commit = self.get_repo().commit()
        # diff = head_commit.diff(head_commit.hexsha + '~1', create_patch=True, ignore_blank_lines=True,
        #            ignore_space_at_eol=True, diff_filter='cr')

        for c in self.get_commits(repo):

            if Commit.objects.filter(hex_sha=c.hexsha).exists():
                continue

            print(c.hexsha)
            # print(c.author)
            commit = Commit()
            commit.repo = self
            commit.author = c.author
            commit.authored_datetime = c.authored_datetime
            commit.message = c.message
            commit.hex_sha = c.hexsha
            commit.bin_sha = c.binsha
            commit.committed_datetime = c.committed_datetime
            commit.count = c.count()

            try:
                # diffs = c.diff(c.hexsha + '~1', create_patch=True, ignore_blank_lines=True,
                #               ignore_space_at_eol=True, diff_filter='cr')
                diffs = c.diff(c.hexsha, create_patch=True, ignore_blank_lines=True,
                               ignore_space_at_eol=True, diff_filter='adm')

                # diff_text = '\n'.join([x.diff for x in diffs])
                diff_text = '\n'.join([str(x) for x in diffs])
                commit.line_additions = len(re.findall('^\+ ', diff_text, re.MULTILINE))
                commit.line_subtractions = len(re.findall('^- ', diff_text, re.MULTILINE))
            except git.GitCommandError:
                pass

            commit.save()
            # print(commit.message)
            # print('Removed: ' + str(commit.line_additions))
            # print('Removed: ' + str(commit.line_subtractions))
            # print(diff_text)


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
