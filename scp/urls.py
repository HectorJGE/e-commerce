"""scp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from scp_app import views


urlpatterns = [
    path('login/',views.LoginView.as_view(),name='login'),
    path('',views.ProductosListView.as_view(),name="Productos"),
    path('productos/<int:pk>',views.ProductosDetailView.as_view(),name='detalle'),
    path('pedido/<pk>',views.DetPedidoTableView.as_view(),name='pedido_detalle'),
    path('pedidos/',views.PedidoTableView.as_view(),name='PedidosList'),
    path('pedidos/all',views.AllPedidosTableView.as_view(),name='TodosLosPedidosList'),
    path('admin/', admin.site.urls),
    path('logout/',views.userLogout.as_view(),name='logout'),
    path('special/',views.special,name='special'),
    path('user_login/',views.user_login,name='user_login'),
    path('add_carrito/<int:id>',views.addCarrito.as_view(),name='add_carrito'),
    path('borrar/<int:id>',views.removeItemCarrito.as_view(),name='removeItemCarrito'),
    path('addpedido/',views.addPedido.as_view(),name='addPedido'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
