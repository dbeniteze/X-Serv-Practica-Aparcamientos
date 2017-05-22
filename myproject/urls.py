
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'aparcamientos.views.inicial'),
    url(r'^parser/', 'aparcamientos.views.parser'),  #para poder utilizar la base
    #url(r'^([a-zA-Z]+[0-9]*)$', "aparcamientos.views.pagina_usuario"),
    url(r'^registro/$','aparcamientos.views.registro'),
    url(r'^login/$','aparcamientos.views.login'),
    url(r'^logout/$', 'aparcamientos.views.logout'),
]
