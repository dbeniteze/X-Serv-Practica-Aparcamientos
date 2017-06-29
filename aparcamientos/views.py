from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Aparcamiento, Comentario, Info_Usuario, Estilo_Personal
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
import bs4
from bs4 import BeautifulSoup, CData
import urllib.request
from django.db.models import Count
from django.template import loader


# Create your views here.
xml_link = str('http://datos.munimadrid.es/portal/site/egob/menuitem.' +
            'ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f22' +
            '01410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=' +
            '202584-0-aparcamientos-residentes&mgmtid=e84276ac109d3410Vg' +
            'nVCM2000000c205a0aRCRD&preview=full')

def parser(request):
    entrada_accesibilidad = Boton_Accesibilidad(flag=False)
    entrada_accesibilidad.save()
    r = urllib.request.urlopen(xml_link).read()
    soup = BeautifulSoup(r, "xml")

    atributos = soup.find_all('contenido')   #atributos es el nombre del tag
    lista_etiquetas = ['ID-ENTIDAD', 'NOMBRE', 'DESCRIPCION', 'ACCESIBILIDAD',
                        'CONTENT-URL', 'NOMBRE-VIA', 'NUM', 'LOCALIDAD',
                        'PROVINCIA', 'CODIGO-POSTAL', 'BARRIO', 'DISTRITO',
                        'LATITUD', 'LONGITUD', 'TELEFONO', 'EMAIL']
    aux_list = []
    for parking in atributos:
        for etiqueta in lista_etiquetas:
            parse_etiqueta = parking.find('atributo', nombre=etiqueta)
            aux_list.append(parse_etiqueta)
        #iteramos la lista por su indice para poder cambiarla
        for elemento in range(len(aux_list)):
            if hasattr(aux_list[elemento], 'string'):
                aux_list[elemento] = aux_list[elemento].string

                if aux_list[elemento] == "1":
                    aux_list[elemento] = True
                if aux_list[elemento] == "0":
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
        aux_list = []


def estilo_personal(user):
    estilo_definido = Estilo_Personal.objects.get(usuario=user)
    return estilo_definido

#def about(request):
#     template = loader.get_template('about.html')




@csrf_exempt
def inicio(request):
    comentarios_parking = Aparcamiento.objects.annotate(numero_comentarios = Count('comentario')).order_by('-numero_comentarios').exclude(numero_comentarios = 0)[:5]
    paginas_personales = Estilo_Personal.objects.all()
    template = loader.get_template('inicio.html')

    if request.user.is_authenticated():
        estilo_visitante = estilo_personal(request.user.username) #informacion del visitante

        context = {
                'aparcamientos_comentados':comentarios_parking,
                'lista_usuarios' : paginas_personales,
                'color': estilo_visitante.color,
                'size': estilo_visitante.tamaño_letra
                }


    else:
        context = {
                'aparcamientos_comentados':comentarios_parking,
                'lista_usuarios' : paginas_personales
                }



    return HttpResponse(template.render(context, request))




def pagina_usuario(request, nombre_user):

    inf_user = Info_Usuario.objects.filter(usuario=nombre_user)  #para obtener los aparcamientos del user
    estilo_user = estilo_personal(nombre_user) #informacion del usuario de la pagina
    template = loader.get_template('pagina_personal.html')

    if request.user.is_authenticated():
        estilo_visitante = estilo_personal(request.user.username) #informacion del visitante

        context = {
            'info_usuario': inf_user,
            'usuario': nombre_user,
            'nombre_pagina': estilo_user.nombre_pagina,  #el nombre de la pagina
            'color': estilo_visitante.color,             #corresponde al usuario de la misma
            'size': estilo_visitante.tamaño_letra
            }
    else:
        context = {
            'info_usuario': inf_user,
            'usuario': nombre_user,
            'nombre_pagina': estilo_user.nombre_pagina
            }

    if request.POST.get('nombre_pagina'):

        estilo_user = estilo_personal(nombre_user)
        estilo_user.nombre_pagina = request.POST['nombre_pagina']
        estilo_user.save(update_fields=['nombre_pagina'])

        estilo_user = estilo_personal(nombre_user)

        mensaje = 'Nombre de la página actualizado'
        context = {
            'info_usuario': inf_user,
            'mensaje' : mensaje,
            'usuario': nombre_user,
            'nombre_pagina': estilo_user.nombre_pagina,
            'size': estilo_user.tamaño_letra,
            'color': estilo_user.color
            }
    if request.POST.get('letra'):
        estilo_user = estilo_personal(nombre_user)
        size_elegido = request.POST['letra']
        estilo_user.tamaño_letra = size_elegido
        estilo_user.save(update_fields=['tamaño_letra'])
        context = {
            'info_usuario': inf_user,
            'usuario': nombre_user,
            'nombre_pagina': estilo_user.nombre_pagina,
            'size': size_elegido,
            'color': estilo_user.color
            }
    if request.POST.get('fondo'):
        estilo_user = estilo_personal(nombre_user)
        fondo_elegido = request.POST['fondo']
        estilo_user.color = fondo_elegido
        estilo_user.save(update_fields=['color'])
        context = {
            'info_usuario': inf_user,
            'usuario': nombre_user,
            'nombre_pagina': estilo_user.nombre_pagina,
            'color': fondo_elegido,
            'size': estilo_user.tamaño_letra
            }


    return HttpResponse(template.render(context, request))

def aparcamientoID(request, ID):
    aparcamientos_filtrados = Aparcamiento.objects.filter(identificador=ID)
    comentario_asociado = Comentario.objects.filter(aparcamiento=aparcamientos_filtrados)
    if request.method == 'GET':
        template = loader.get_template('aparcamientoID.html')


        if request.user.is_authenticated():
            estilo_visitante = estilo_personal(request.user.username) #informacion del visitante
            template = loader.get_template('aparcamientoID.html')
            context = {
                'aparcamientos': aparcamientos_filtrados,
                'comentarios': comentario_asociado,
                'color': estilo_visitante.color,
                'size': estilo_visitante.tamaño_letra
                }
        else:
            context = {
                'aparcamientos': aparcamientos_filtrados,
                'comentarios': comentario_asociado
                }
    if request.method == 'POST':
        template = loader.get_template('aparcamientoID.html')
        aparcamiento_concreto = Aparcamiento.objects.get(identificador=ID)

        if request.POST.get('comentario'): #se envia un comentario sobre el aparcamiento
            comentario = request.POST['comentario']
            Comentario.objects.create(comentario= comentario,
                                      aparcamiento= aparcamiento_concreto)
            comentario_asociado = Comentario.objects.filter(aparcamiento=aparcamientos_filtrados)

            if request.user.is_authenticated():
                estilo_visitante = estilo_personal(request.user.username) #informacion del visitante
                context = {
                    'aparcamientos': aparcamientos_filtrados,
                    'comentarios': comentario_asociado,
                    'color': estilo_visitante.color,
                    'size': estilo_visitante.tamaño_letra
                    }
            else:
                context = {
                    'aparcamientos': aparcamientos_filtrados,
                    'comentarios': comentario_asociado
                    }
        if request.POST.get('puntuacion'):
            aparcamiento_concreto.puntuacion += 1
            aparcamiento_concreto.save(update_fields=['puntuacion'])

            context = {
                'aparcamientos': aparcamientos_filtrados,
                'comentarios': comentario_asociado
                }
        else: #corresponde a la seleccion de un aparcamiento
            park_user = Info_Usuario.objects.filter(usuario=request.user.username) #buscamos los parkings del usuario
            try:

                aparcamiento_añadido = park_user.get(aparcamiento__identificador = ID) #buscamos el parking concreto
                mensaje = 'El aparcamiento ya fue seleccionado anteriormente'


            except Info_Usuario.DoesNotExist:  #si no existe previamente ese aparcamiento para el usuario
                pass                           #se crea
                Info_Usuario.objects.create(usuario = request.user.username,
                                            aparcamiento = aparcamiento_concreto)

                mensaje = "parking seleccionado"

            if request.user.is_authenticated():
                estilo_visitante = estilo_personal(request.user.username) #informacion del visitante
                context = {
                    'mensaje': mensaje,
                    'aparcamientos': aparcamientos_filtrados,
                    'comentarios': comentario_asociado,
                    'color': estilo_visitante.color,
                    'size': estilo_visitante.tamaño_letra
                    }
            else:
                context = {
                    'aparcamientos': aparcamientos_filtrados,
                    'comentarios': comentario_asociado,
                    'mensaje': mensaje
                    }
    return HttpResponse(template.render(context, request))



@csrf_exempt
def barra_aparcamientos(request):

    template = loader.get_template('aparcamientos.html')
    if request.method == 'GET':
        aparcamientos = Aparcamiento.objects.all()
        if request.user.is_authenticated():
            estilo_visitante = estilo_personal(request.user.username) #informacion del visitante
            context = {
                'aparcamientos': aparcamientos,
                'color': estilo_visitante.color,
                'size': estilo_visitante.tamaño_letra
                }
        else:
            context = {
                'aparcamientos': aparcamientos
                }
    if request.method == 'POST':
        if request.POST.get('accessibilidad'):
            aparcamientos_accesibles = Aparcamiento.objects.filter(access=True)

            if request.user.is_authenticated():
                estilo_visitante = estilo_personal(request.user.username) #informacion del visitante
                context = {
                    'aparcamientos': aparcamientos_accesibles,
                    'color': estilo_visitante.color,
                    'size': estilo_visitante.tamaño_letra
                    }
            else:
                context = {
                    'aparcamientos': aparcamientos_filtrados
                    }

        else:
            filtro_distrito = request.POST['distrito']
            try:
                aparcamientos_filtrados = Aparcamiento.objects.filter(distrito=filtro_distrito)
            except Exception as e:
                raise "EXCEPCION"#aparcamientos_filtrados = aparcamientos


            if request.user.is_authenticated():
                estilo_visitante = estilo_personal(request.user.username) #informacion del visitante
                context = {
                    'aparcamientos': aparcamientos_filtrados,
                    'color': estilo_visitante.color,
                    'size': estilo_visitante.tamaño_letra
                    }
            else:
                context = {
                    'aparcamientos': aparcamientos_filtrados
                    }



    return HttpResponse(template.render(context, request))



def registro(request):
    template = loader.get_template('registro.html')
    if request.method=='POST':
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid:
            formulario.save()
            Estilo_Personal.objects.create(usuario = request.POST['username'],
                                           nombre_pagina = 'Página de ' + request.POST['username'])
            return HttpResponseRedirect('/')
    else:
        formulario = UserCreationForm()
        context = {'formulario': formulario}
    return HttpResponse(template.render(context, request))
