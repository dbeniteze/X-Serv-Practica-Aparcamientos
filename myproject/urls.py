
from django.conf.urls import include, url
from django.contrib.auth.views import login, logout
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'aparcamientos.views.inicio'),
    url(r'^aparcamientos/$', 'aparcamientos.views.barra_aparcamientos'),
    url(r'^parser/', 'aparcamientos.views.parser'),  #para poder utilizar la base
    url(r'^([a-zA-Z]+[0-9]*)$', "aparcamientos.views.pagina_usuario"),
    url(r'^registro/$','aparcamientos.views.registro'),
    url(r'^login/', login),
    url(r'^logout/', logout, {'next_page': '/'}),
    url(r'^aparcamientos/([0-9]+)$', "aparcamientos.views.aparcamientoID"),
    url(r'^about/', "aparcamientos.views.about")
]
