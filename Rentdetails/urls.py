from django.conf.urls import patterns, url

from Rentdetails import views

# maps urls
urlpatterns = patterns('',
    url(r'^(?P<rentdetail_id>\d+)$', views.editrentdetails, name='editrentdetails'),
    #url(r'^HOspcf/(?P<houseowner_id>\d+)/$', views.detail, name='detail')
    
)