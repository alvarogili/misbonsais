from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$','principal.views.ingresar'),
    url(r'^guia/$','principal.views.guia'),    
    url(r'^bonsai/(?P<id_bonsai>\d+)$','principal.views.detalle_bonsai'),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT,}),
    url(r'^usuario/bonsai/nuevo/$','principal.views.nuevo_bonsai'),
    url(r'^bonsai/editar/(?P<id_bonsai>\d+)$','principal.views.editar_bonsai'),
    url(r'^bonsai/borrar/(?P<id_bonsai>\d+)$','principal.views.borrar_bonsai'),
    url(r'^bonsai/nuevaLabor/(?P<id_bonsai>\d+)$','principal.views.nueva_labor'),
    url(r'^labor/borrar/(?P<id_labor>\d+)$', 'principal.views.borrar_labor'),
    url(r'^usuario/$', 'principal.views.main_usuario'),
    url(r'^usuarios/nuevo$', 'principal.views.nuevo_usuario'),
    url(r'^usuarios/envio_pass$', 'principal.views.envio_pass'),
    url(r'^usuario/editar/$', 'principal.views.editar_usuario'),
    url(r'^usuario/cambiar_contr/$', 'principal.views.cambiar_contr'),
    url(r'^usuario/salir/$', 'principal.views.logout'),
)
