from django.conf.urls import patterns, url, include

from Rentdetails import views
from Rentdetails.rentdetailsapi import RentDetailsResource

entry_resource = RentDetailsResource()
# maps urls
urlpatterns = patterns('',
    url(r'^(?P<rentdetail_id>\d+)/info$', views.inforentdetails, name='inforentdetails'),
    url(r'^(?P<rentdetail_id>\d+)/edit$', views.editrentdetails, name='editrentdetails'),
    url(r'^(?P<renterinfo_id>\d+)/addnew$', views.addrentdetails, name='addrentdetails'),
    url(r'^(?P<rentdetail_id>\d+)/delete$', views.delete_rent_detail, name='delete_rent_detail'),
    url(r'^(?P<flag>\d+)/submit$', views.submitrentdetails, name='submitrentdetails'),
    (r'^rentdetailsapi/', include(entry_resource.urls))
    #url(r'^HOspcf/(?P<houseowner_id>\d+)/$', views.detail, name='detail')
    
)