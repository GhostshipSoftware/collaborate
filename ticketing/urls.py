from django.conf.urls.defaults import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from collaborate.ticketing import views

urlpatterns = patterns('collaborate.ticketing.views',
    url(r'^tickets/$', views.TicketListView.as_view()),
    url(r'^tickets/(?P<pk>[0-9]+)/$', views.TicketDetailView.as_view()),
    url(r'^tickets/(?P<pk>[0-9]+)/comments/', views.TicketCommentView.as_view()),
    url(r'^ticketqueues/$', views.TicketQueueListView.as_view()),
    url(r'^ticketqueues/(?P<pk>[0-9]+)/$', views.TicketQueueDetailView.as_view()),
    url(r'^ticketqueues/(?P<pk>[0-9]+)/tickets/$', views.TicketQueueTicketListView.as_view()),
)
urlpatterns = format_suffix_patterns(urlpatterns)
