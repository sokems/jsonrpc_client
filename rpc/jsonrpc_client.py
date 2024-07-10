import json
import requests
from django.conf import settings
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
import ssl


class TLSAdapter(HTTPAdapter):
    def __init__(self, cert, key, *args, **kwargs):
        self.cert = cert
        self.key = key
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=self.cert, keyfile=self.key)
        kwargs['ssl_context'] = context
        return PoolManager(*args, **kwargs)


class JSONRPCClient:
    def __init__(self, url, cert, key):
        self.url = url
        self.cert = cert
        self.key = key
        self.session = requests.Session()
        self.session.mount('https://', TLSAdapter(cert, key))

    def call_method(self, method, params=None):
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
            "id": 1
        }
        response = self.session.post(self.url, json=payload)
        return response.json()


# Пример использования клиента
if __name__ == "__main__":
    url = "https://slb.medv.ru/api/v2/"
    client = JSONRPCClient(url, settings.CERTIFICATE, settings.PRIVATE_KEY)
    response = client.call_method("auth.check")
    print("Response:", json.dumps(response, indent=4))