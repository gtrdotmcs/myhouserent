from django.conf.urls import patterns, url, include
from houseowner.houserentapi import HouseownerResource, UserResource
from houseowner import views    
from tastypie.api import Api

v1_api = Api(api_name='v1')
v1_api.register(HouseownerResource())
v1_api.register(UserResource())
# maps urls
urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^HOspcf/(?P<houseowner_id>\d+)/details$', views.detail, name='detail'),
    (r'^api/', include(v1_api.urls)),
    #url(r'^HOspcf/formview$', views.countries_view, name='countries_view')
    
)