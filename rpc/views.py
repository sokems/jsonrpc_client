from django.views.generic import FormView
from django.shortcuts import render
from .forms import JSONRPCForm
from .jsonrpc_client import JSONRPCClient
from django.conf import settings
import json

class JSONRPCView(FormView):
    template_name = 'rpc/jsonrpc_form.html'
    form_class = JSONRPCForm
    success_url = '/'

    def form_valid(self, form):
        method = form.cleaned_data['method']
        params = form.cleaned_data['params']
        if params:
            try:
                params = json.loads(params)
            except json.JSONDecodeError:
                params = {}

        client = JSONRPCClient("https://slb.medv.ru/api/v2/", settings.CERTIFICATE, settings.PRIVATE_KEY)
        response = client.call_method(method, params)
        return render(self.request, self.template_name, {'form': form, 'response': json.dumps(response, indent=4)})

    def form_invalid(self, form):
        return super().form_invalid(form)