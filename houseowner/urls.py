from django.conf.urls import patterns, url

from houseowner import views

# maps urls
urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^HOspcf/(?P<houseowner_id>\d+)/$', views.detail, name='detail')
    
)