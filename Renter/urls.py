from django.conf.urls import patterns, url

from Renter import views

# maps urls
urlpatterns = patterns('',
    url(r'^(?P<renter_id>\d+)$', views.showdetails, name='showdetails'),
    url(r'^(?P<houseowner_id>\d+)/addnew$', views.addrenterinfo, name='addrenterinfo'),
    url(r'^(?P<renter_id>\d+)/edit$', views.editrenterinfo, name='editrenterinfo'),
    url(r'^(?P<flag>\d+)/submit$', views.submitrentinfo, name='submitrentinfo'),
    #url(r'^HOspcf/(?P<houseowner_id>\d+)/$', views.detail, name='detail')
)