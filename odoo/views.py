# Librerias django python
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout

# Create your views here.
from django.http import HttpResponse

#Accesos de Odoo
with open('./secrets/url.txt') as a:
    url = a.read().strip()
with open('./secrets/db.txt') as b:
    db = b.read().strip()
with open('./secrets/username.txt') as c:
    username = c.read().strip()
with open('./secrets/password.txt') as d:
    password = d.read().strip()

import xmlrpc.client
import json

# Intento de conexión a la base de datos de Odoo
try:
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))

    common.version()
    print("Version: \n",json.dumps(common.version(), indent=4),"\n")
    uid = common.authenticate(db, username, password, {})

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
except Exception as e:
        print(f"An error occurred: {e}")

# Vista principal /odoo
# Lee y envia los registros del modelo "Journal" (Diarios) de Odoo.
# No tiene función alguna, solo es Test, disponible para cambios    
@api_view(['GET'])
def index(request):

    m = models.execute_kw(db, uid, password, 'account.move', 'search_read', [[]], {'fields': ['name', 'journal_id'], 'limit': 2000})

    return Response(m)

# Vista polizas /odoo/gpolizas
# Comprueba si hay un usuario autenticado, en caso de ser verdadero hace otra comprobación
# Comprueba si el usuario es "admin", en caso de ser verdadero arroja todas las polizas existentes de la base de datos Odoo
# En caso de ser falso, solo arroja las polizas del respectivo usuario
@api_view(['GET'])
def get_polizas(request):
    # Comprobar si esta autenticado
    if request.user.is_authenticated:
        # Para usuarios autenticados
        # Comprobar si es "admin" -> Desplega todos los registros de polizas
        if request.user.username == "admin":
            # Recoge todas las polizas existentes
            y = models.execute_kw(db, uid, password, 'x_polizas', 'search_read', [[]], {'fields': ['x_name', 'x_studio_servicio', 'x_studio_num', 'x_studio_fecha_inicio', 'x_studio_fecha_expiro', 'x_studio_cliente', 'x_studio_equipos', 'x_studio_tipo'], 'limit': 2000})
        # Si es falso -> Solo desplega las polizas de el usuario autenticado
        else: 
            # Busca el cliente del usuario coincidente a la base de datos de Odoo
            x = models.execute_kw(db, uid, password, 'x_usuarios', 'search_read', [[['x_name', '=', request.user.username]]], {'fields': ['x_studio_cliente'], 'limit': 2000})
            # Recoge las polizas coincidentes al cliente
            y = models.execute_kw(db, uid, password, 'x_polizas', 'search_read', [[['x_studio_cliente', '=', x[0]['x_studio_cliente'][1]]]], {'fields': ['x_name', 'x_studio_servicio', 'x_studio_num', 'x_studio_fecha_inicio', 'x_studio_fecha_expiro', 'x_studio_cliente', 'x_studio_equipos', 'x_studio_tipo'], 'limit': 2000})

        # Arroja las polizas obtenidas
        return Response(y)
    # Si no esta autenticado, arroja "Nope" como respuesta
    else:
        # Para usuarios no autenticados
        return HttpResponse("Nope")
        
# Vista polizas /odoo/gps
# Recoge el numero enviado por el front, comprueba si el numero existe
# Desplega la poliza solicitada por "numero"
@api_view(['GET'])
def gpoliza_s(request):
    # Recoge en una variable "numero"
    numero = request.GET.get("numero")
    
    # Comprueba si "numero" existe
    if numero:
        # Pide a Odoo la poliza coincidente a "numero"
        x = models.execute_kw(db, uid, password, 'x_polizas', 'search_read', [[['x_studio_num', '=', str(numero)]]], {'fields': ['x_name', 'x_studio_servicio', 'x_studio_num', 'x_studio_fecha_inicio', 'x_studio_fecha_expiro', 'x_studio_cliente', 'x_studio_equipos', 'x_studio_tipo'], 'limit': 2000})
        # Devuelve los datos de la poliza al front
        return Response(x[0])
    else:
    # En caso de que no exista "numero"
        return HttpResponse("Nope")
        
# Vista polizas /odoo/ges
# Recoge el numero enviado por el front, comprueba si el numero existe
# Desplega todos los equipos de la poliza solicitada por "numero"
@api_view(['GET'])
def gequipo_s(request):
    # Recoge en una variable "numero"
    numero = request.GET.get("numero")

    # Comprueba si "numero" existe
    if numero:
        # Pide a Odoo la poliza coincidente a "numero"
        x = models.execute_kw(db, uid, password, 'x_polizas', 'search_read', [[['x_studio_num', '=', str(numero)]]], {'fields': ['x_name', 'x_studio_servicio', 'x_studio_tipo', 'x_studio_num', 'x_studio_fecha_inicio', 'x_studio_fecha_expiro', 'x_studio_cliente', 'x_studio_equipos', 'x_studio_tipo'], 'limit': 2000})
        # Pide a Odoo los equipos coincidentes a la poliza
        y = models.execute_kw(db, uid, password, 'x_equipos_de_poliza', 'search_read', [[['x_studio_poliza', '=', x[0]['x_name']]]], {'fields': ['x_name', 'x_studio_marca', 'x_studio_modelo', 'x_studio_serie'], 'limit': 2000})

        # Devuelve los datos de los equipos al front
        return Response(y)
    else:
    # En caso de que no exista "numero"
        return HttpResponse("Nope")
        
# Vista polizas /odoo/ge
# Recoge el numero enviado por el front, comprueba si el numero existe
# Desplega el equipo solicitado por el numero "idenf"
@api_view(['GET'])
def gequipo(request):
    # Recoge en una variable "idenf"
    idenf = request.GET.get("idenf")
    
    # Comprueba si "idenf" existe
    if idenf:
        # Pide a Odoo el equipo coincidente a "idenf"
        y = models.execute_kw(db, uid, password, 'x_equipos_de_poliza', 'search_read', [[['x_name', '=', str(idenf)]]], {'fields': ['x_name', 'x_studio_tipo', 'x_studio_marca', 'x_studio_modelo', 'x_studio_serie'], 'limit': 2000})

        # Devuelve los datos del equipo al front
        return Response(y[0])
    else:
    # En caso de que no exista "idenf"
        return HttpResponse("Nope")
        
# Vista polizas /odoo/grs
# Recoge el numero enviado por el front, comprueba si el numero existe
# Desplega todos los reportes solicitados por el numero "idenf"
@api_view(['GET'])
def greporte_s(request):
    # Recoge en una variable "idenf"
    idenf = request.GET.get("idenf")

    # Comprueba si "idenf" existe
    if idenf:
        # Pide a Odoo los reportes coincidentes a "idenf"
        y = models.execute_kw(db, uid, password, 'x_reportes_poliza', 'search_read', [[['x_studio_equipo', '=', str(idenf)]]], {'fields': [
        #Datos del equipo
        'x_name', 'x_studio_equipo', 
        'x_studio_tipo', 'x_studio_poliza', 
        'x_studio_serie', 'x_studio_modelo',
        'x_studio_parte',
        #Datos del cliente 
        'x_studio_encargado', 'x_studio_area', 
        'x_studio_direccion',
        #Datos del servicio
        'x_studio_tecnico', 'x_studio_folio',
        'x_studio_fecha_mantenimiento', 'x_studio_siguiente_mantenimiento',
        'x_studio_mantenimiento_asignado', 'x_studio_revision',
        'x_studio_reemplazo',
        #Reporte
        'x_studio_otros', 'x_studio_falla',
        'x_studio_observaciones', 'x_estado',
        ], 'limit': 2000})

        # Devuelve los datos de los reportes al front
        return Response(y)
    else:
    # En caso de que no exista "idenf"
        return HttpResponse("Nope")

# Vista polizas /odoo/gr
# Recoge el numero enviado por el front, comprueba si el numero existe
# Desplega el reportes solicitado por el numero "idenf"
@api_view(['GET'])
def greporte(request):
    # Recoge en una variable "idenf"
    idenf = request.GET.get("idenf")
    
    # Comprueba si "idenf" existe
    if idenf:
        # Pide a Odoo el reporte coincidente al numero "idenf"
        y = models.execute_kw(db, uid, password, 'x_reportes_poliza', 'search_read', [[['x_name', '=', str(idenf)]]], {'fields': [
        #Datos del equipo
        'x_name', 'x_studio_equipo', 
        'x_studio_tipo', 'x_studio_poliza', 
        'x_studio_serie', 'x_studio_modelo',
        'x_studio_parte',
        #Datos del cliente 
        'x_studio_encargado', 'x_studio_area', 
        'x_studio_direccion',
        #Datos del servicio
        'x_studio_tecnico', 'x_studio_folio',
        'x_studio_fecha_mantenimiento', 'x_studio_siguiente_mantenimiento',
        'x_studio_mantenimiento_asignado', 'x_studio_revision',
        'x_studio_reemplazo',
        #Checklist Mantenimiento
        'x_studio_c_limpieza_interna', 'x_studio_c_limpieza_externa', 
        #Impresoras
        'x_studio_c_cabezal', 'x_studio_rodillo',
        'x_studio_bandas', 'x_studio_c_sensores',
        'x_studio_c_configuracion', 'x_studio_c_presion',
        'x_studio_c_calidad', 'x_studio_c_otros',
        #Control de Acceso
        'x_studio_c_bateria', 'x_studio_c_lectoras',
        'x_studio_c_chapa', 'x_studio_c_montaje', 
        'x_studio_c_cableado', 'x_studio_c_pluma',
        #APC
        'x_studio_c_filtros', 'x_studio_c_firmware',
        'x_studio_desague', 'x_studio_c_red',
        #Reporte
        'x_studio_otros', 'x_studio_falla',
        'x_studio_observaciones', 'x_estado',
        'x_studio_reporte',
        #Nombre y firma
        'x_studio_nombre', 'x_studio_firma',
        #Evidencia fotografica
        #Antes
        'x_studio_foto1_a', 'x_studio_foto2_a',
        'x_studio_foto3_a', 'x_studio_foto4_a',
        'x_studio_foto5_a',
        #Despues
        'x_studio_foto1_d', 'x_studio_foto2_d',
        'x_studio_foto3_d', 'x_studio_foto4_d',
        'x_studio_foto5_d',
        ], 'limit': 2000})

        # Devuelve al front todos los datos del reporte
        return Response(y[0])
    else:
    # En caso de que no exista "idenf"
        return HttpResponse("Nope")

# Vista polizas /odoo/polizas
# Arroja todas las polizas existentes en el sistema Odoo
# Sin uso, solo pruebas, puede eliminarse o aprovecharse
@api_view(['GET'])
def polizas(request):
    
    #Busca y recoge todos los registros del modelo polizas
    y = models.execute_kw(db, uid, password, 'x_polizas', 'search_read', [[]], {'fields': ['x_name', 'x_studio_servicio', 'x_studio_num', 'x_studio_fecha_inicio', 'x_studio_fecha_expiro', 'x_studio_cliente', 'x_studio_equipos', 'x_studio_tipo'], 'limit': 2000})

    # Arroja los registros obtenidos 
    return Response(y)
    
# Vista polizas /odoo/equipos
# Arroja todos los equipos existentes en el sistema Odoo
# Sin uso, solo pruebas, puede eliminarse o aprovecharse
@api_view(['GET'])
def equipos(request):
        
    # Busca y recoge todos los registros del modelo equipos de poliza
    x = models.execute_kw(db, uid, password, 'x_equipos_de_poliza', 'search_read', [[]], {'fields': ['x_name', 'x_studio_tipo', 'x_studio_marca', 'x_studio_modelo', 'x_studio_serie'], 'limit': 2000})
    # Arroja los registros obtenidos
    return Response(x)


# Vista autenticación /odoo/login
# Recoge los accesos proporcionados, se autentica y en caso de ser exitoso se inicia sesión
def login_v(request):
    # Recoge en variables los accesos proporcionados
    user = request.GET.get("user")
    passs = request.GET.get("pass")

    # Declara la funcion para autenticar en una variable
    tryauth = authenticate(username=user, password=passs)
    # Si la autenticación falla
    if not tryauth:
        print(f"Error en las credenciales {user} {passs}")
        return HttpResponse("NoAuth")
    # Si fue exitosa continua el codigo, se inicia sesión
    login(request, tryauth)
    print("Autenticado")
    return HttpResponse("Autenticado")
    # No backend authenticated the credentials
        
# Vista autenticación /odoo/usercheck
# Comprueba si el cliente esta autenticado
def usercheck(request):
    # Verifica si esta autenticado
    if request.user.is_authenticated:
        # En caso de ser asi, devuelve el username del usuario
        return HttpResponse(request.user.username)
    else:
        #En caso de no estarlo
        return HttpResponse("Nope")

# Vista autenticación /odoo/logout
# Cierra sesión
def logout_v(request):
    logout(request)

    return HttpResponse("SESSION CLOSED")

# Vista polizas /odoo/reportes
# Recoge todos los reportes existentes en Odoo
# Sin uso, solo pruebas, puede eliminarse o aprovecharse
@api_view(['GET'])
def getALLreportes(request):
    x = models.execute_kw(db, uid, password, 'x_reportes_poliza', 'search_read', [[]], {'fields': [
         #Datos del equipo
         'x_name', 'x_studio_equipo', 
         'x_studio_tipo', 'x_studio_poliza', 
         'x_studio_serie', 'x_studio_modelo',
         'x_studio_parte',
         #Datos del cliente 
         'x_studio_encargado', 'x_studio_area', 
         'x_studio_direccion',
         #Datos del servicio
         'x_studio_tecnico', 'x_studio_folio',
         'x_studio_fecha_mantenimiento', 'x_studio_siguiente_mantenimiento',
         'x_studio_mantenimiento_asignado', 'x_studio_revision',
         'x_studio_reemplazo',
         #Checklist 
         'x_studio_c_limpieza_interna', 'x_studio_c_limpieza_externa', 
         'x_studio_c_cabezal', 'x_studio_rodillo',
         'x_studio_bandas', 'x_studio_c_sensores',
         'x_studio_c_configuracion', 'x_studio_c_presion',
         'x_studio_c_calidad', 'x_studio_c_otros',
         #Reporte
         'x_studio_otros', 'x_studio_falla',
         'x_studio_observaciones', 'x_estado',
         ], 'limit': 2000})
    return Response(x)