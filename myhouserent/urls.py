from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myhouserent.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^user/', include('loginapp.urls', namespace="loginapp")),
    url(r'^houseowner/', include('houseowner.urls', namespace="houseowner")),
    url(r'^renterinfo/', include('Renter.urls', namespace="Renter")), 
    url(r'^rentdetails/', include('Rentdetails.urls', namespace="Rentdetails")), 
    url(r'^admin/', include(admin.site.urls)),
)
