from scp_app.models import DetalleCarrito,Carrito,Pedido

def cart_det(request):

    if request.user.is_active:
        rol_ped=False
        if request.user.has_perm('scp_app.Pedido_vista'):
            rol_ped=True
        mostrar=True
        carrito=Carrito.objects.filter(cliente_carrito=request.user)
        Car_det=DetalleCarrito.objects.filter(carrito=carrito.last())
        pedido=Pedido.objects.filter(carrito=carrito.last())
        if pedido or not len(Car_det):
            mostrar=False
        cant=len(Car_det)
        return {'carrito_detalle':Car_det,'mostrar':mostrar,'cant_d':cant,'ped_vista':rol_ped}
    return{}
