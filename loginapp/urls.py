from django.conf.urls import patterns, url
import loginapp
#from loginapp import views

# maps urls
urlpatterns = patterns('',
    url(r'^$', 'loginapp.views.login_user'),
    #url(r'^HOspcf/(?P<houseowner_id>\d+)/$', views.detail, name='detail')
    
)