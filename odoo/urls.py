from django.urls import path

from . import views

urlpatterns = [
    #path("", views.index, name="index"),
    path('invoices/', views.index, name='invoices'),
    path('polizas/', views.polizas, name='polizas'),
    path('gpolizas/', views.get_polizas, name='get_polizas'),
    path('gps/', views.gpoliza_s, name='gps'),
    path('ges/', views.gequipo_s, name='ges'),
    path('ge/', views.gequipo, name='ge'),
    path('grs/', views.greporte_s, name="grs"),
    path('gr/', views.greporte, name="gr"),
    path('equipos/', views.equipos, name='equipos'),
    path('login/', views.login_v, name='login'),
    path('logout/', views.logout_v, name='logout'),
    path('usercheck/', views.usercheck, name='home'),
    path('reportes/', views.getALLreportes, name="reportes"),
]