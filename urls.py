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
    url(r'^', include('collaborate.tasklist.urls')),
    url(r'^', include('collaborate.ticketing.urls')),
    url(r'^', include('collaborate.chat.urls')),
    url(r'^', include('collaborate.billing.urls')),
    url(r'^', include('collaborate.issue_tracker.urls')),
    url(r'^logout/', 'collaborate.chat.views.logout_view'),
    url(r'^accounts/login/', 'django.contrib.auth.views.login'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^manage/', 'collaborate.views.manage'),
    url(r'^detail/user/', 'collaborate.views.user_detail'),
    url(r'^', 'collaborate.views.index'),
)
