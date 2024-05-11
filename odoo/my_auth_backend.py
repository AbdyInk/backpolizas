from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

import xmlrpc.client
import json

User = get_user_model()

url = 'https://vito-technologies.odoo.com'
db = 'vito-technologies'
un = 'ventas@vitotechnologies.com'
pw = '4dm1n!'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, un, pw, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))


#common.version()
#print("Version: \n",json.dumps(common.version(), indent=4),"\n")


class MyAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Aquí es donde debes implementar tu lógica de autenticación.
        user_list = models.execute_kw(db, uid, pw, 'x_usuarios', 'search_read', [[]], {'fields': ['x_name', 'x_studio_pass'], 'limit': 2000})
        # Luego, busca al usuario en tu lista:
        for user_dict in user_list:
            if user_dict['x_name'] == username and user_dict['x_studio_pass'] == password:
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    user = User.objects.create_user(username=username, password=password)
                return user  
                

        # Si el usuario no se encuentra en la lista, retorna None
        return None
