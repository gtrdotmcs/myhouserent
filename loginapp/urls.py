from django.conf.urls import patterns, url
import loginapp
#from loginapp import views

# maps urls
urlpatterns = patterns('',
    url(r'^login/$', 'loginapp.views.login_user'),
     url(r'^logout/$', 'loginapp.views.logout_view'),
    #url(r'^HOspcf/(?P<houseowner_id>\d+)/$', views.detail, name='detail')
    
)