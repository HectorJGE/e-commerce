from django.views.generic import View,TemplateView,ListView,DetailView, CreateView, DeleteView, UpdateView
from . import models
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from scp_app.models import DetalleCarrito
from datatableview.views import DatatableView
from datatableview import Datatable, columns
from scp_app.mixins import ValidarPermisosMixins

class LoginView(TemplateView):
        template_name = "login.html"

class ProductosListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    context_object_name = 'ProductosList'
    model = models.Producto
    template_name = 'Productos/ProductosList.html'

    def get_queryset(self):
        nombre_p=self.request.GET.get('producto')
        if nombre_p:
            producto=models.Producto.objects.filter(nombre_producto__icontains=nombre_p).order_by('-nombre_producto')
        else:
            producto=models.Producto.objects.all().order_by('-nombre_producto')
        return producto


class PedidosListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    context_object_name = 'PedidosList'
    model = models.Pedido
    template_name = 'Pedidos/PedidosList.html'


class ProductosDetailView(LoginRequiredMixin,DetailView):
    login_url = '/login/'
    context_object_name = 'producto_detalle'
    model=models.Producto
    template_name = "Productos/ProductoDetalle.html"


class CarritoListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    context_object_name = 'Carrito_detalle'
    model = DetalleCarrito
    template_name = 'base/base.html'

class addCarrito(View):

    def post(self, request, id):
        carrito=models.Carrito.objects.filter(cliente_carrito=request.user).last()
        Pedido=models.Pedido.objects.filter(carrito=carrito)
        cantidad=request.POST.get('cantidad')
        if Pedido:
            cart = models.Carrito.objects.create(cliente_carrito=request.user)
            models.DetalleCarrito.objects.create(carrito=cart, producto=models.Producto.objects.get(pk=id),
                                                  cantidad_producto=cantidad)
        else:
            if not carrito:
                carrito = models.Carrito.objects.create(cliente_carrito=request.user)
            models.DetalleCarrito(carrito=carrito, producto=models.Producto.objects.get(pk=id),
                                   cantidad_producto=cantidad).save()
        return redirect(reverse('Productos'))

class removeItemCarrito(View):

    def get(self,request,id):
        cart = models.Carrito.objects.filter(cliente_carrito=request.user).last()
        instance = models.DetalleCarrito.objects.filter(carrito=cart)
        producto = models.Producto.objects.get(pk=id)
        instance.filter(producto=producto).delete()
        return redirect(reverse('Productos'))

class addPedido(View):

    def get(self,request):
        cart = models.Carrito.objects.filter(cliente_carrito=request.user).last()
        total_pedido = get_total(models.DetalleCarrito.objects.filter(carrito=cart))
        ped = models.Pedido.objects.create(carrito=cart, total_pedido=total_pedido)
        return HttpResponseRedirect(reverse('pedido_detalle', kwargs={'pk': ped.pk}))

def get_total(model):
    sum=0
    for item in model:
        sum+=item.producto.precio_venta
    return sum

def user_login(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username,password=password)
            if user:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect(reverse('Productos'))
                else:
                    return HttpResponse("Cuenta no activa")
            else:
                print("Error al intentar iniciar sesion")
                return render(request,'login.html',{'error':'Datos Incorrectos'})

        else:
            return render(request,'login.html',{})

class userLogout(View):
    def get(self,request):
        logout(request)
        return HttpResponseRedirect(reverse('login'))



@login_required
def special(request):
    return HttpResponse("Estas logueado Nice")
class PedidoDataTable(Datatable):
    ver=columns.DisplayColumn(('Detalle'), processor='detail')
    class Meta:
        model=models.Pedido
        columns = ['id','total_pedido','date']

    @staticmethod
    def detail(instance, view, *args, **kwargs):
        detail_url = reverse('pedido_detalle', args=[int(instance.pk)])
        return """<a href="{}">Ver mas</a>
                """.format( detail_url)

class PedidoTableView(LoginRequiredMixin,DatatableView):
    login_url = '/login/'
    datatable_class = PedidoDataTable
    template_name = 'Pedidos/PedidosList.html'
    def get_queryset(self):
        return models.Pedido.objects.filter(carrito__cliente_carrito=self.request.user)


class DetPedidoDataTable(Datatable):
    ver=columns.DisplayColumn(('Precio'), processor='precio')

    class Meta:
        model = models.DetalleCarrito
        columns = ['producto','cantidad_producto']
    @staticmethod
    def precio(instance, view, *args, **kwargs):
        return instance.producto.precio_venta
class DetPedidoTableView(LoginRequiredMixin,DatatableView):
    login_url = '/login/'
    datatable_class = DetPedidoDataTable
    template_name = 'Pedidos/PedidoDetalle.html'

    def get_queryset(self):
        pedido=models.Pedido.objects.get(pk=self.kwargs['pk'])
        return models.DetalleCarrito.objects.filter(carrito=pedido.carrito)

    def get_context_data(self, **kwargs):
        context = super(DetPedidoTableView, self).get_context_data(**kwargs)
        context['pedido_detalle'] = models.Pedido.objects.get(pk=self.kwargs['pk'])
        return context

class AllPedidosDataTable(Datatable):
    user=columns.DisplayColumn(('Usuario'), processor='usuario')
    ver=columns.DisplayColumn(('Detalle'), processor='detail')
    class Meta:
        model=models.Pedido
        columns = ['id','total_pedido','date']

    @staticmethod
    def detail(instance, view, *args, **kwargs):
        id_pk = int(instance.pk)
        detail_url = reverse('pedido_detalle', args=[id_pk])
        return """<a href="{}">Ver mas</a>
                """.format( detail_url)
    @staticmethod
    def usuario(instance, view, *args, **kwargs):
        return instance.carrito.cliente_carrito
class AllPedidosTableView(ValidarPermisosMixins,LoginRequiredMixin,DatatableView):
    login_url = '/login/'
    datatable_class = AllPedidosDataTable
    template_name = 'Pedidos/AllPedidosList.html'
    permission_required = ('scp_app.Pedido_vista')
    model=models.Pedido
