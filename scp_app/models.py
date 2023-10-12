from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    cedula = models.PositiveIntegerField(unique=True)
    direccion = models.CharField(max_length=256, blank=True)
    nro_telefono = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Producto(models.Model):
    nombre_producto = models.CharField(max_length=256)
    cantidad_stock = models.PositiveIntegerField(default=0)
    precio_costo = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion_producto = models.CharField(max_length=256, blank=True)
    imagen_producto = models.ImageField(upload_to='producto_pics', blank=True,
                                        default='../static/imagen_por_defecto.jpeg')

    def __str__(self):
        return self.nombre_producto

class Carrito(models.Model):
    cliente_carrito = models.ForeignKey(User, on_delete=models.CASCADE,null=True)

class Pedido(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, null=True)
    date = models.DateField(("Fecha"), default=datetime.date.today,null=True)
    total_pedido= models.IntegerField(default=0,null=True)
@receiver(post_save, sender=Pedido)
def act_stock(sender, instance, **kwargs):
    DetalleCarrito.objects.filter()
    for det in DetalleCarrito.objects.filter(carrito=instance.carrito):
        prod = Producto.objects.get(pk=det.producto.pk)
        prod.cantidad_stock -= det.cantidad_producto
        prod.save()

class DetalleCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_producto = models.PositiveIntegerField(default=0)
