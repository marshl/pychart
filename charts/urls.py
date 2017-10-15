from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.repo_list, name='repo_list'),
    url(r'^repo/(?P<pk>\d+)/$', views.repo_detail, name='repo_detail'),
    url(r'^repo/(?P<pk>\d+)/reload$', views.repo_reload, name='repo_reload'),
    url(r'^repo/(?P<pk>\d+)/reset', views.repo_reset, name='repo_reset'),
    url(r'^repo/(?P<pk>\d+)/get_repo_author_total', views.get_repo_author_total, name='get_repo_author_total'),
]
