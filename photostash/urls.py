from django.conf.urls import patterns, include, url

from photostash import api


urlpatterns = patterns('',
    url(r'^api/', include(api.v1.urls)),
)
