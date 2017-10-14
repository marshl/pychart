from django.shortcuts import render, get_object_or_404
from .models import Repository


# Create your views here.
def repo_list(request):
    repos = Repository.objects.all().order_by('title')
    return render(request, 'charts/repo_list.html', {'repos': repos})


def repo_detail(request, pk):
    repo = get_object_or_404(Repository, pk=pk)
    return render(request, 'charts/repo_detail.html', {'repo': repo})
