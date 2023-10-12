from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages

class ValidarPermisosMixins(object):
    permission_required = ('scp_app.Pedido_vista')
    url_redirect = None
    def get_perms(self):
        if isinstance(self.permission_required,str):return (self.permission_required)
        else: return self.permission_required

    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse_lazy('Productos')
        return self.get_url_redirect
