from django.conf.urls import patterns, url

from houseowner import views

# maps urls
urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^HOspcf/(?P<houseowner_id>\d+)/details$', views.detail, name='detail'),
    #url(r'^HOspcf/formview$', views.countries_view, name='countries_view')
    
)