from django.conf.urls import patterns, url, include
from houseowner.houserentapi import HouseownerResource
from houseowner import views

entry_resource = HouseownerResource()
# maps urls
urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^HOspcf/(?P<houseowner_id>\d+)/details$', views.detail, name='detail'),
    (r'^houseownerapi/', include(entry_resource.urls)),
    #url(r'^HOspcf/formview$', views.countries_view, name='countries_view')
    
)