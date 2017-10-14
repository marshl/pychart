from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.repo_list, name='repo_list'),
    url(r'^repo/(?P<pk>\d+)/$', views.repo_detail, name='repo_detail'),
]
