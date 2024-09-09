from django.urls import path

from . import views

urlpatterns = [
    #path("", views.index, name="index"),
    path('invoices/', views.index, name='invoices'),
    path('servicios/', views.servicios, name='servicios'),
    path('polizas/', views.polizas, name='polizas'),
    path('gpolizas/', views.get_polizas, name='get_polizas'),
    path('gss/', views.gservicio_s, name='gss'),
    path('gs/', views.gservicio, name='gs'),
    path('gssgp/', views.gservicio_s_gpoliza, name='gssgp'),
    path('grsgs/', views.greporte_s_gservicio, name='grsgs'),
    path('gesgs/', views.gequipo_s_gservicio, name='gesgs'),
    path('gps/', views.gpoliza_s, name='gps'),
    path('ges/', views.gequipo_s, name='ges'),
    path('ge/', views.gequipo, name='ge'),
    path('grs/', views.greporte_s, name="grs"),
    path('gr/', views.greporte, name="gr"),
    path('gruser/', views.greporte_s_user, name="gruser"),
    path('equipos/', views.equipos, name='equipos'),
    path('login/', views.login_v, name='login'),
    path('logout/', views.logout_v, name='logout'),
    path('usercheck/', views.usercheck, name='home'),
    path('reportes/', views.getALLreportes, name="reportes"),
    path('wasdfalse/', views.get_client_ip_address, name="lol")
]