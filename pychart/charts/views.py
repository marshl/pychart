from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .models import Repository
import time
from datetime import datetime, timedelta, timezone, date


# Create your views here.
def repo_list(request):
    repos = Repository.objects.all().order_by("title")
    return render(request, "charts/repo_list.html", {"repos": repos})


def repo_detail(request, pk):
    repo = get_object_or_404(Repository, pk=pk)
    return render(request, "charts/repo_detail.html", {"repo": repo})


def repo_reload(request, pk):
    repo = get_object_or_404(Repository, pk=pk)
    repo.load_commits()
    return redirect("repo_detail", pk=pk)


def repo_reset(request, pk):
    repo = get_object_or_404(Repository, pk=pk)
    repo.delete_commits()
    return redirect("repo_detail", pk=pk)


def get_repo_author_total(request, pk):
    repo = get_object_or_404(Repository, pk=pk)
    authors = pd.Series([x.author for x in repo.commit_set.all()])
    series = authors.value_counts()
    d = series.to_dict()

    result = {
        "cols": [
            {"id": "", "label": "Author", "pattern": "", "type": "string"},
            {"id": "", "label": "Commits", "pattern": "", "type": "number"},
        ],
        "rows": [{"c": [{"v": x}, {"v": int(d[x])}]} for x in d],
    }

    return JsonResponse(result, safe=False)


def get_commits_per_day(request, pk):
    repo = get_object_or_404(Repository, pk=pk)
    commits = pd.Series([x.committed_datetime.date() for x in repo.commit_set.all()])
    # series = commits.value_counts()
    df = pd.DataFrame({"commit_date": commits})
    series = df.groupby("commit_date").size().asfreq("1d", fill_value=0)
    d = series.to_dict()

    # repo = get_object_or_404(Repository, pk=pk)
    # # commits = pd.Series([x.committed_datetime for x in repo.commit_set.all()])
    # # series = commits.value_counts()
    # commits = repo.commit_set.all()
    # df = pd.DataFrame({'commit_date': pd.Series([x.committed_datetime for x in commits])})
    # for author in set([x.author for x in commits]):
    #     df[author] = pd.Series([x.committed_datetime for x in commits if x.author == author])
    #
    # series = df.groupby('commit_date').size().asfreq('1d', fill_value=0)
    # d = series.to_dict()

    result = {
        "cols": [
            {"id": "", "label": "Date", "pattern": "", "type": "date"},
            {"id": "", "label": "Commits Per Day", "pattern": "", "type": "number"},
        ],
        "rows": [{"c": [{"v": date_to_json(x)}, {"v": int(d[x])}]} for x in d],
    }

    return JsonResponse(result, safe=False)


def get_commit_frequency(request, pk):
    repo = get_object_or_404(Repository, pk=pk)
    # df = pd.DataFrame()
    days = 7
    hours = 24
    # df['hours'] = pd.Series([hour for day in range(days) for hour in range(hours)])
    # df['days'] = pd.Series([day for hour in range(hours) for day in range(days)])

    commits = [0 for day in range(days) for hour in range(hours)]
    for commit in repo.commit_set.all():
        d = commit.committed_datetime + timedelta(seconds=time.localtime().tm_gmtoff)
        day = d.weekday()
        hour = d.hour
        commits[day * hours + hour] += 1

    result = {
        "cols": [
            {"id": "", "label": "Commits", "pattern": "", "type": "string"},
            {"id": "", "label": "Hour", "pattern": "", "type": "number"},
            {"id": "", "label": "Day", "pattern": "", "type": "number"},
            {"id": "", "label": "Commits", "pattern": "", "type": "number"},
            {"id": "", "label": "Commits", "pattern": "", "type": "number"},
        ],
        "rows": [
            {
                "c": [
                    {"v": str(commits[day * hours + hour])},
                    {"v": hour, "f": f"{hour}:00"},
                    {"v": day + 1, "f": date(2001, 1, day + 1).strftime("%A")},
                    {
                        "v": commits[day * hours + hour]
                        if commits[day * hours + hour] > 0
                        else None
                    },
                    {"v": commits[day * hours + hour]},
                ]
            }
            for day in range(days)
            for hour in range(hours)
        ],
    }

    return JsonResponse(result, safe=False)


def date_to_json(date):
    return date.strftime(f"Date(%Y, %m, %d, 0, 0, 0)")
