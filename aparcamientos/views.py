from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Aparcamiento
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth import authenticate, login, logout
from bs4 import BeautifulSoup, CData
import urllib.request


# Create your views here.
xml_link = str('http://datos.munimadrid.es/portal/site/egob/menuitem.' +
            'ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f22' +
            '01410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=' +
            '202584-0-aparcamientos-residentes&mgmtid=e84276ac109d3410Vg' +
            'nVCM2000000c205a0aRCRD&preview=full')

def parser(xml_doc):
    r = urllib.request.urlopen(xml_link).read()
    soup = BeautifulSoup(r, "xml")

    atributos = soup.find_all('contenido')   #atributos es el nombre del tag

    for parking in atributos:

        parse_id = parking.find('atributo', nombre='ID-ENTIDAD')
        parse_nombre = parking.find('atributo', nombre='NOMBRE')
        parse_descripcion = parking.find('atributo', nombre='DESCRIPCION')
        parse_access = parking.find('atributo', nombre='ACCESIBILIDAD')
        parse_url = parking.find('atributo', nombre='CONTENT-URL')
        parse_calle = parking.find('atributo', nombre='NOMBRE-VIA')
        parse_num_via = parking.find('atributo', nombre='NUM')
        parse_localidad = parking.find('atributo', nombre='LOCALIDAD')
        parse_provincia = parking.find('atributo', nombre='PROVINCIA')
        parse_codigo_postal = parking.find('atributo', nombre='CODIGO-POSTAL')
        parse_barrio = parking.find('atributo', nombre='BARRIO')
        parse_distrito = parking.find('atributo', nombre='DISTRITO')
        parse_latitud = parking.find('atributo', nombre='LATITUD')
        parse_longitud = parking.find('atributo', nombre='LONGITUD')
        parse_tlf = parking.find('atributo', nombre='TELEFONO')
        parse_mail = parking.find('atributo', nombre='EMAIL')


        aux_list = [parse_id, parse_nombre, parse_descripcion, parse_access,
                        parse_url, parse_calle, parse_num_via, parse_localidad,
                        parse_provincia, parse_codigo_postal, parse_barrio,
                        parse_distrito,  parse_latitud, parse_longitud,
                        parse_tlf, parse_mail,]

        #iteramos la lista por su indice para poder cambiarla
        for elemento in range(len(aux_list)):
            if hasattr(aux_list[elemento], 'string'):
                aux_list[elemento] = aux_list[elemento].string

                if aux_list[elemento] == 1:
                    aux_list[elemento] = True
                if aux_list[elemento] == 0:
                    aux_list[elemento] = False

            else:
                aux_list[elemento] = ""

        nueva_entrada = Aparcamiento(identificador=aux_list[0],
                                     nombre = aux_list[1],
                                     descripcion = aux_list[2],
                                     access = aux_list[3],
                                     url = aux_list[4],
                                     calle = aux_list[5],
                                     numero_via = aux_list[6],
                                     localidad = aux_list[7],
                                     provincia = aux_list[8],
                                     codigo_postal = aux_list[9],
                                     barrio = aux_list[10],
                                     distrito = aux_list[11],
                                     latitud = aux_list[12],
                                     longitud = aux_list[13],
                                     tlf = aux_list[14],
                                     mail = aux_list[15])
        nueva_entrada.save()
