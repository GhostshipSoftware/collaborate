from django.conf.urls.defaults import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from tasklist import views

urlpatterns = patterns('collaborate.tasklist.views',
    url(r'^tasklists/$', views.TaskListListView.as_view()),
    url(r'^tasklists/(?P<pk>[0-9]+)/$', views.TaskListDetail.as_view()),
    url(r'^tasklists/(?P<pk>[0-9]+)/tasks/$', views.TaskListTasksView.as_view()),
    url(r'^tasklists/account/(?P<pk>[0-9]+)/$', views.AccountTaskListView.as_view()),
    url(r'^tasks/$', views.TasksList.as_view()),
    url(r'^tasks/(?P<pk>[0-9]+)/$', views.TasksListDetail.as_view()),
    url(r'^todo/$', views.index),

)

urlpatterns = format_suffix_patterns(urlpatterns)
