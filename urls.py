from __future__ import unicode_literals
from rest_framework.compat import patterns, url
from django.conf.urls.defaults import include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'collaborate.views.home', name='home'),
    # url(r'^collaborate/', include('collaborate.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('tasklist.urls')),
    url(r'^', include('ticketing.urls')),
    url(r'^', include('chat.urls')),
    url(r'^', include('billing.urls')),
    url(r'^', include('issue_tracker.urls')),
    url(r'^logout/', 'chat.views.logout_view'),
    url(r'^accounts/login/', 'django.contrib.auth.views.login'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^manage/', 'views.manage'),
    url(r'^detail/user/', 'views.user_detail'),
    url(r'^', 'views.index'),
)
