from django.conf.urls import patterns, url

from houseowner import views
<<<<<<< HEAD

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
     url(r'^(?P<houseowner_id>\d+)/$', views.detail, name='detail'),
=======
# maps urls
urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<houseowner_id>\d+)/$', views.detail, name='detail')
    
>>>>>>> fe47f3919c1d7d4d42e1fadbfa0968e18650adbe
)