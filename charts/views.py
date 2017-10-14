from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
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

    


    result = {
        "cols": [
            {"id": "", "label": "Topping", "pattern": "", "type": "string"},
            {"id": "", "label": "Slices", "pattern": "", "type": "number"}
        ],
        "rows": [
            {"c": [{"v": "Mushrooms", "f": None}, {"v": 3, "f": None}]},
            {"c": [{"v": "Onions", "f": None}, {"v": 1, "f": None}]},
            {"c": [{"v": "Olives", "f": None}, {"v": 1, "f": None}]},
            {"c": [{"v": "Zucchini", "f": None}, {"v": 1, "f": None}]},
            {"c": [{"v": "Pepperoni", "f": None}, {"v": 2, "f": None}]}
        ]
    }

    return JsonResponse(result, safe=False)
