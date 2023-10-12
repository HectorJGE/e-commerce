from django.contrib import admin
from scp_app.models import Producto,UserProfile,Pedido,DetalleCarrito,Carrito
from django.contrib.auth.models import Permission
# Register your models here.
admin.site.register(Permission)
admin.site.register(Producto)
admin.site.register(UserProfile)
admin.site.register(Pedido)
admin.site.register(DetalleCarrito)
admin.site.register(Carrito)