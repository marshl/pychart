from django.shortcuts import render
from .models import Repository
from django.utils import timezone


# Create your views here.
def repo_list(request):
    repos = Repository.objects.all().order_by('title')
    return render(request, 'charts/repo_list.html', {'repos': repos})
