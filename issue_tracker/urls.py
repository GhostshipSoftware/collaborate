from django.conf.urls.defaults import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from issue_tracker import views

urlpatterns = patterns('collaborate.issue_tracker.views',
    url(r'^issue_managers/', views.IssueManagerListView.as_view()),
    url(r'^issue_managers/(?P<pk>[0-9]+)/', views.IssueManagerDetailView.as_view()),
    url(r'^issues/(?P<pk>[0-9]+)/', views.IssueListView.as_view()),
    url(r'^issues/', views.issues_client_index),

)
