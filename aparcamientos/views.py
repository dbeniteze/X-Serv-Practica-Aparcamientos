from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Aparcamiento, Comentario, Info_Usuario
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth import authenticate, login as log_in, logout as log_out
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
        aux_list = []

@csrf_exempt
def inicio(request):
    comentarios_parking = Aparcamiento.objects.annotate(numero_comentarios = Count('comentario')).order_by('-numero_comentarios').exclude(numero_comentarios = 0)[:5]

    paginas_personales = Info_Usuario.objects.all()
    lista_usuarios = []
    lista_info_personal = []
    for u in paginas_personales:
        if u.usuario not in lista_usuarios:
            lista_usuarios.append(u.usuario)
            lista_info_personal.append([u.usuario, u.pagina_personal])

    template = loader.get_template('inicio.html')
    context = {
        'aparcamientos_comentados':comentarios_parking,
        #'pags_personales':paginas_personales,
        'lista_usuarios' : lista_info_personal
        }

    return HttpResponse(template.render(context, request))




def pagina_usuario(request, nombre_user):

    inf_user = Info_Usuario.objects.filter(usuario=nombre_user)

    template = loader.get_template('pagina_personal.html')
    context = {
        'info_usuario': inf_user,
        'usuario': nombre_user
        }

    return HttpResponse(template.render(context, request))

def aparcamientoID(request, ID):
    if request.method == 'GET':
        template = loader.get_template('aparcamientoID.html')

        aparcamientos_filtrados = Aparcamiento.objects.filter(identificador=ID)
        comentario_asociado = Comentario.objects.filter(aparcamiento=aparcamientos_filtrados)

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
            mensaje= "comentario enviado"
            context = {
                'mensaje': mensaje
                }
        else: #corresponde a la seleccion de un aparcamiento

            Info_Usuario.objects.create(usuario = request.user.username,
                                        aparcamiento = aparcamiento_concreto)



            mensaje= "parking seleccionado"
            context = {
                'mensaje': mensaje
                }
    return HttpResponse(template.render(context, request))



@csrf_exempt
def barra_aparcamientos(request):

    if request.method == 'GET':
        template = loader.get_template('aparcamientos.html')

        aparcamientos = Aparcamiento.objects.all()
        context = {
            'aparcamientos': aparcamientos
            }
    if request.method == 'POST':
        template = loader.get_template('aparcamientos.html')
        filtro_distrito = request.POST['distrito']
        try:
            aparcamientos_filtrados = Aparcamiento.objects.filter(distrito=filtro_distrito)
        except Exception as e:
            raise "NO ENCUENTRA DISTRITO"

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
            return HttpResponseRedirect('/')
    else:
        formulario = UserCreationForm()
        context = {'formulario': formulario}
    return HttpResponse(template.render(context, request))
