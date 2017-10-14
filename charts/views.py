from django.shortcuts import render


# Create your views here.
def repo_list(request):
    return render(request, 'charts/repo_list.html', {})
