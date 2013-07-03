from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    #url(r'^laboratory/test/$', 'laboratory.views.test'),
    #url(r'^laboratory/pages/', include('django.contrib.flatpages.urls')),   
    url(r'^laboratory/study/(?P<study>\d+)/$',	'laboratory.views.study', name="study"),
	url(r'^laboratory/page/(?P<page>[\w-]+)/$', 'laboratory.views.page',  name="lab_page"), 
    url(r'^laboratory/$', 						'laboratory.views.home',  name="labs"),   
    
)

