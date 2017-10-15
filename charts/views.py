from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .models import Repository


# Create your views here.
def repo_list(request):
    repos = Repository.objects.all().order_by('title')
    return render(request, 'charts/repo_list.html', {'repos': repos})


def repo_detail(request, pk):
    repo = get_object_or_404(Repository, pk=pk)
    return render(request, 'charts/repo_detail.html', {'repo': repo})


def repo_reload(request, pk):
    repo = get_object_or_404(Repository, pk=pk)
    repo.load_commits()
    return redirect('repo_detail', pk=pk)


def repo_reset(request, pk):
    repo = get_object_or_404(Repository, pk=pk)
    repo.delete_commits()
    return redirect('repo_detail', pk=pk)


def get_chart_data(request):
    repo = Repository.objects.all()[1]
    # authors = []
    # for c in repo.commit_set.all():
    #     authors.append(c.author)
    #
    # print(authors)
    authors = pd.Series([x.author for x in repo.commit_set.all()])
    df = pd.DataFrame({'count': 1, 'author': authors})
    series = df.groupby('author')['count'].sum()

    result = {
        "cols": [
            {"id": "", "label": "Author", "pattern": "", "type": "string"},
            {"id": "", "label": "Commits", "pattern": "", "type": "number"}
        ],
        'rows': series_to_rows(series)
        # "rows": [
        #     {"c": [{"v": "Andrew Pigram", "f": None}, {"v": 27, "f": None}]},
        #     {"c": [{"v": "Liam Marshall", "f": None}, {"v": 160, "f": None}]},
        #     {"c": [{"v": "Vegemash", "f": None}, {"v": 9, "f": None}]},
        #     {"c": [{"v": "prathyusha sama", "f": None}, {"v": 4, "f": None}]},
        # ]
    }

    return JsonResponse(result, safe=False)


def series_to_rows(series: pd.Series):
    d = series.to_dict()
    return [{'c': [{'v': x}, {'v': int(d[x])}]} for x in d]
