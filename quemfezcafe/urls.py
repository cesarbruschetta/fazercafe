# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import RedirectView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


PATH_STATIC = settings.PATH_STATIC

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'quemfezcafe.app.views.home', name='home'),
    # url(r'^quemfezcafe/', include('quemfezcafe.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Autenticação	
    url(r'^login/$', RedirectView.as_view(url='/login/google-oauth2/'), name='login'),
    url(r'^logout/$','django.contrib.auth.views.logout_then_login',name='logout'),
    
    url(r'', include('social_auth.urls')),

	#servir arquivos estaticos CSS / JS / IMG
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': PATH_STATIC, 'show_indexes': False}),    
)
