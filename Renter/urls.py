from django.conf.urls import patterns, url

from Renter import views

# maps urls
urlpatterns = patterns('',
    url(r'^(?P<renter_id>\d+)$', views.editdetails, name='editdetails'),
    #url(r'^HOspcf/(?P<houseowner_id>\d+)/$', views.detail, name='detail')
    
)