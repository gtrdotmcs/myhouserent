from django.conf.urls import patterns, url

from Rentdetails import views

# maps urls
urlpatterns = patterns('',
    url(r'^(?P<rentdetail_id>\d+)/info$', views.inforentdetails, name='inforentdetails'),
    url(r'^(?P<rentdetail_id>\d+)/edit$', views.editrentdetails, name='editrentdetails'),
    url(r'^(?P<rentdetail_id>\d+)/submit$', views.submitrentdetails, name='submitrentdetails'),
    #url(r'^HOspcf/(?P<houseowner_id>\d+)/$', views.detail, name='detail')
    
)