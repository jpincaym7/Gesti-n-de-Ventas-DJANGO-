from datetime import date,datetime
from decimal import Decimal,ROUND_HALF_UP
import random
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
import os
import django
from django.db.models import F,Q
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, Avg, Max, Min, Count
from django.db.models.functions import Substr
from argparse import Namespace
# Establece la configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proy_sales.settings')
# Inicializa Django
django.setup()
from django.contrib.auth.models import User
from core.models import Brand, Supplier, Product, Category, Customer, PaymentMethod, Invoice, InvoiceDetail
def probar_orm():
    #py manage.py sqlmigrate core 0001 # presenta el codigo sql a migrar
    #py manage.py showmigrations # mustra las migraciones realizadas
    def create_user(create=False):  # Define la función create_user con dos_plus  parámetros opcionales
        if create:  # Comprueba si create es True
            User.objects.create_user(  # Crea un nuevo usuario con los siguientes detalles
                username='susan',  # Establece el nombre de usuario
                password='susan123',  # Establece la contraseña
                email='susan@example.com'  # Establece el correo electrónico
            )
            users = User.objects.all()  # Recupera todos los usuarios de la base de datos y los almacena en la variable users

            print("Listado de Usuarios")
            print(users)
        
    create_user(True)
    def script_brands(create=False):
        if create:
            user= User.objects.get(username='dverap')
            brand1 = Brand.objects.create(description="Nike", user=user)
            brand2 = Brand.objects.create(description="Arroz Flor", user=user,state=False)
            brand3 = Brand.objects.create(description="Atun Real", user=user)
            brand4 = Brand.objects.create(description="Azucar Valdez", user=user)
            brand5 = Brand.objects.create(description="Samsung", user=user)
        print("Listado de las marcas")
        brands= Brand.objects.all()
        print(brands)
        brands= Brand.active_brands.all()
        for brand in brands: print(brand,brand.state) 
    script_brands(True)
        
    def scripts_category(create=False):
        if create:
            user= User.objects.get(id=1)
            cat = Category(description='electrodomesticos',user=user)
            cat.save()
            Category(description='Atun',user=user).save()
        print("Listado de Categorias")
        print(Category.objects.all())
    scripts_category(True)
    def scripts_payment_Method(create=False):
        if create:
            user= User.objects.get(pk=1)
            PaymentMethod.objects.bulk_create([ 
            PaymentMethod(description="Contado",user=user), 
            PaymentMethod(description="Credito",user=user), 
            PaymentMethod(description="Tarjeta",user=user) 
            ]) 
        print("Listado de los Metodos de Pagos")
        print(PaymentMethod.objects.all())
    scripts_payment_Method(True)
    def scripts_customer(create=False):
        if create:
            user= User.objects.get(pk=1)
            Customer.objects.bulk_create([ 
            Customer(dni='0914192182',first_name='Daniel',last_name='Vera',address='Milagro',gender='M',date_of_birth=datetime.date(1970, 5, 21),user=user), 
            Customer(dni='0914192184',first_name='Miguel',last_name='Berrones',address='9 de Octubre',gender='M',date_of_birth=datetime.date(2017, 10, 10),user=user), 
            Customer(dni='0914192185',first_name='Yady',last_name='Bohorquez',address='Pedro Carbo',gender='F',date_of_birth=datetime.date(1975, 7, 10),user=user) 
            ]) 
        
        print("Listado de los Clientes")
        customers= Customer.objects.values('id','dni','first_name','last_name')
        customers2= Customer.objects.values_list('id','dni','first_name','last_name')
        print(customers)
        print(customers2)
        print(list(customers))
        print(list(customers2))
    scripts_customer(True)
probar_orm()