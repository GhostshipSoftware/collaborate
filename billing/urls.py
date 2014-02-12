from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import patterns, url, include
from billing import views

urlpatterns = patterns('billing.views',
    url(r'^tokens/', views.ObtainAuthToken.as_view()),
    url(r'^accounts/$', views.AccountListView.as_view()),
    url(r'^accounts/(?P<pk>[0-9]+)/users/', views.AccountCreateUser.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/', views.UserDetailView.as_view()),
)
urlpatterns = format_suffix_patterns(urlpatterns)

