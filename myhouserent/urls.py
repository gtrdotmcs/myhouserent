from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

# Django testypie version 2
from tastypie.api import Api
from houseowner.houserentapi import HouseownerResource, UserResource
from Renter.renterapi import RenterResource
from Rentdetails.rentdetailsapi import RentDetailsResource

v2_api = Api(api_name='v2')
v2_api.register(UserResource())
v2_api.register(HouseownerResource())
v2_api.register(RenterResource())
v2_api.register(RentDetailsResource())
# Django testypie version 2

urlpatterns = patterns('',
    # Examples:
     url(r'^$', 'myhouserent.views.mainindex', name='mainindex'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^user/', include('loginapp.urls', namespace="loginapp")),
    url(r'^houseowner/', include('houseowner.urls', namespace="houseowner")),
    url(r'^renterinfo/', include('Renter.urls', namespace="Renter")), 
    url(r'^rentdetails/', include('Rentdetails.urls', namespace="Rentdetails")), 
    url(r'^admin/', include(admin.site.urls)),
    (r'^api/', include(v2_api.urls)), # Django testypie version 2
)

urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
