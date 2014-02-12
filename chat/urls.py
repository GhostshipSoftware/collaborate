from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns
from chat import views

urlpatterns = patterns('chat.views',
    url(r'^chat/channel/', views.channel),
    url(r'^chat/', views.chat),
    url(r'^channels/$', views.ChannelListView.as_view()),
    url(r'^channels/(?P<pk>[0-9]+)/users/$', views.ChannelUserAddView.as_view()),
    url(r'^channels/(?P<pk>[0-9]+)/remove/$', views.ChannelRemoveUserView.as_view()),
    url(r'^channels/(?P<pk>[0-9]+)/messages/$', views.MessageCreateView.as_view()),
    url(r'^channels/(?P<pk>[0-9]+)/$', views.ChannelDetailView.as_view()),
)
urlpatterns = format_suffix_patterns(urlpatterns)
