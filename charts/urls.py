from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.repo_list, name='repo_list'),
]
