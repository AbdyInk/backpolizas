from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout


# Create your views here.
from django.http import HttpResponse

url = 'https://vito-technologies.odoo.com'
db = 'vito-technologies'
username = 'ventas@vitotechnologies.com'
password = '4dm1n!'

import xmlrpc.client
import json

try:
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))

    common.version()
    print("Version: \n",json.dumps(common.version(), indent=4),"\n")
    uid = common.authenticate(db, username, password, {})

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
except Exception as e:
        print(f"An error occurred: {e}")
    
@api_view(['GET'])
def index(request):

    #Buscar y sobreescribir registros y campos del modelo Stock de Inventario
    m = models.execute_kw(db, uid, password, 'account.move', 'search_read', [[]], {'fields': ['name', 'journal_id'], 'limit': 2000})

    #z= ""
    #for x in y:
        #z += f"{x} <br>"

    return Response(m)

@api_view(['GET'])
def get_polizas(request):
    
        #Buscar y sobreescribir registros y campos del modelo Stock de Inventario
        if request.user.is_authenticated:
        # Do something for authenticated users.
            if request.user.username == "admin":
                y = models.execute_kw(db, uid, password, 'x_polizas', 'search_read', [[]], {'fields': ['x_name', 'x_studio_num', 'x_studio_fecha_inicio', 'x_studio_fecha_expiro', 'x_studio_cliente', 'x_studio_equipos', 'x_studio_tipo'], 'limit': 2000})
            else: 
                x = models.execute_kw(db, uid, password, 'x_usuarios', 'search_read', [[['x_name', '=', request.user.username]]], {'fields': ['x_studio_cliente'], 'limit': 2000})
                y = models.execute_kw(db, uid, password, 'x_polizas', 'search_read', [[['x_studio_cliente', '=', x[0]['x_studio_cliente'][1]]]], {'fields': ['x_name', 'x_studio_num', 'x_studio_fecha_inicio', 'x_studio_fecha_expiro', 'x_studio_cliente', 'x_studio_equipos', 'x_studio_tipo'], 'limit': 2000})

            return Response(y)
        else:
        # Do something for anonymous users.
            return HttpResponse("Nope")
        
@api_view(['GET'])
def gpoliza_s(request):
        numero = request.GET.get("numero")
        #request.GET.get("numero")
        #Buscar y sobreescribir registros y campos del modelo Stock de Inventario
        if numero:
        # Do something for authenticated users.
            x = models.execute_kw(db, uid, password, 'x_polizas', 'search_read', [[['x_studio_num', '=', str(numero)]]], {'fields': ['x_name', 'x_studio_num', 'x_studio_fecha_inicio', 'x_studio_fecha_expiro', 'x_studio_cliente', 'x_studio_equipos', 'x_studio_tipo'], 'limit': 2000})
        #x = models.execute_kw(db, uid, password, 'x_equipos_poliza', 'search_read', [[]], {'fields': ['x_name'], 'limit': 2000})
        #z = y
        #z += x
        #for x in y:
            #z += json.dumps(x, indent=4)

        #print(json.dumps(y, indent=4))

            return Response(x[0])
        else:
        # Do something for anonymous users.
            return HttpResponse("Nope")
        
@api_view(['GET'])
def gequipo_s(request):
        numero = request.GET.get("numero")
        #request.GET.get("numero")
        #Buscar y sobreescribir registros y campos del modelo Stock de Inventario
        if numero:
        # Do something for authenticated users.
            x = models.execute_kw(db, uid, password, 'x_polizas', 'search_read', [[['x_studio_num', '=', str(numero)]]], {'fields': ['x_name', 'x_studio_tipo', 'x_studio_num', 'x_studio_fecha_inicio', 'x_studio_fecha_expiro', 'x_studio_cliente', 'x_studio_equipos', 'x_studio_tipo'], 'limit': 2000})
            y = models.execute_kw(db, uid, password, 'x_equipos_de_poliza', 'search_read', [[['x_studio_poliza', '=', x[0]['x_name']]]], {'fields': ['x_name', 'x_studio_marca', 'x_studio_modelo', 'x_studio_serie'], 'limit': 2000})
        #x = models.execute_kw(db, uid, password, 'x_equipos_poliza', 'search_read', [[]], {'fields': ['x_name'], 'limit': 2000})
        #z = y
        #z += x
        #for x in y:
            #z += json.dumps(x, indent=4)

        #print(json.dumps(y, indent=4))

            return Response(y)
        else:
        # Do something for anonymous users.
            return HttpResponse("Nope")
        
@api_view(['GET'])
def gequipo(request):
        idenf = request.GET.get("idenf")
        #request.GET.get("numero")
        #Buscar y sobreescribir registros y campos del modelo Stock de Inventario
        if idenf:
        # Do something for authenticated users.
            y = models.execute_kw(db, uid, password, 'x_equipos_de_poliza', 'search_read', [[['x_name', '=', str(idenf)]]], {'fields': ['x_name', 'x_studio_tipo', 'x_studio_marca', 'x_studio_modelo', 'x_studio_serie'], 'limit': 2000})
        #x = models.execute_kw(db, uid, password, 'x_equipos_poliza', 'search_read', [[]], {'fields': ['x_name'], 'limit': 2000})
        #z = y
        #z += x
        #for x in y:
            #z += json.dumps(x, indent=4)

        #print(json.dumps(y, indent=4))

            return Response(y[0])
        else:
        # Do something for anonymous users.
            return HttpResponse("Nope")
        
@api_view(['GET'])
def greporte_s(request):
        idenf = request.GET.get("idenf")
        #request.GET.get("numero")
        #Buscar y sobreescribir registros y campos del modelo Stock de Inventario
        if idenf:
        # Do something for authenticated users.

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
        #x = models.execute_kw(db, uid, password, 'x_equipos_poliza', 'search_read', [[]], {'fields': ['x_name'], 'limit': 2000})
        #z = y
        #z += x
        #for x in y:
            #z += json.dumps(x, indent=4)

        #print(json.dumps(y, indent=4))

            return Response(y)
        else:
        # Do something for anonymous users.
            return HttpResponse("Nope")

@api_view(['GET'])
def greporte(request):
        idenf = request.GET.get("idenf")
        #request.GET.get("numero")
        #Buscar y sobreescribir registros y campos del modelo Stock de Inventario
        if idenf:
        # Do something for authenticated users.

            x = models.execute_kw(db, uid, password, 'ir.attachment', 'search_read', [[['res_name', '=', str(idenf)]]], {'fields': ['datas', 'res_name'], 'limit': 2})

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
        #x = models.execute_kw(db, uid, password, 'x_equipos_poliza', 'search_read', [[]], {'fields': ['x_name'], 'limit': 2000})
        #z = y
        #z += x
        #for x in y:
            #z += json.dumps(x, indent=4)

            z = y+x

        #print(json.dumps(y, indent=4))

            return Response(y[0])
        else:
        # Do something for anonymous users.
            return HttpResponse("Nope")

@api_view(['GET'])
def polizas(request):
    
        #Buscar y sobreescribir registros y campos del modelo Stock de Inventario
        y = models.execute_kw(db, uid, password, 'x_polizas', 'search_read', [[]], {'fields': ['x_name', 'x_studio_num', 'x_studio_fecha_inicio', 'x_studio_fecha_expiro', 'x_studio_cliente', 'x_studio_equipos', 'x_studio_tipo'], 'limit': 2000})
        #x = models.execute_kw(db, uid, password, 'x_equipos_poliza', 'search_read', [[]], {'fields': ['x_name'], 'limit': 2000})
        #z = y
        #z += x
        #for x in y:
            #z += json.dumps(x, indent=4)

        #print(json.dumps(y, indent=4))
        return Response(y)
    #except Exception as e:
        #return HttpResponse(f"An error occurred: {e}")
    

@api_view(['GET'])
def equipos(request):
        #request.GET.getlist('a')
        #Buscar y sobreescribir registros y campos del modelo Stock de Inventario
        x = models.execute_kw(db, uid, password, 'x_equipos_de_poliza', 'search_read', [[]], {'fields': ['x_name', 'x_studio_tipo', 'x_studio_marca', 'x_studio_modelo', 'x_studio_serie'], 'limit': 2000})
        return Response(x)
#except Exception as e:
        #return HttpResponse(f"An error occurred: {e}")

#@api_view(['GET'])
def login_v(request):
    user = request.GET.get("user")
    passs = request.GET.get("pass")

    tryauth = authenticate(username=user, password=passs)
    if not tryauth:
    # A backend authenticated the credentials
        print(f"Error en las credenciales {user} {passs}")
        return HttpResponse("NoAuth")
    login(request, tryauth)
    print("Autenticado")
    return HttpResponse("Autenticado")
    # No backend authenticated the credentials
        
    
def usercheck(request):
    if request.user.is_authenticated:
    # Do something for authenticated users.
        return HttpResponse(request.user.username)
    else:
    # Do something for anonymous users.
        return HttpResponse("Nope")
    
def logout_v(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponse("idk")

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