from http import HTTPStatus

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from scp_app.models import Producto, Carrito, DetalleCarrito


# Create your tests here.

class ProductoTest(TestCase):
    def setUp(self):
        self.user=User.objects.create_user(username='Enrique',password='enrique123')
        self.producto=Producto.objects.create(nombre_producto="Lapiz",cantidad_stock=10,precio_costo=300,precio_venta=1000,descripcion_producto="Lapiz de papel fabercastell 2B")

    def test_carrito(self):
        self.client.force_login(self.user)
        response=self.client.post("/add_carrito/1", data={'cantidad':3})
        self.assertEqual(response.status_code,HTTPStatus.FOUND)
        self.assertEqual(Carrito.objects.all().count(),1)

    def test_login(self):
        response=self.client.post("/user_login/",data={'username':'Enrique','password':'enrique123'})
        self.assertEqual(response.status_code,HTTPStatus.FOUND)

    def test_eliminar(self):
        self.client.force_login(self.user)
        response=self.client.get(reverse('removeItemCarrito',kwargs={'id':self.producto.pk}))
        self.assertEqual(response.status_code,HTTPStatus.FOUND)

    def test_pedido(self):
        self.client.force_login(self.user)
        response=self.client.get(reverse('addPedido'))
        self.assertEqual(response.status_code,HTTPStatus.FOUND)

