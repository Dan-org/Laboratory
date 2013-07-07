from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',


    url(r'^laboratory/', 	include('laboratory.urls')),
    url(r'^admin/', 		include(admin.site.urls)),

    # Auth
    url(r'^auth/', include('django.contrib.auth.urls')),
    
    url(r'^$', 'example.views.home', name='home'),
)
