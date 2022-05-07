import json
from django.contrib import auth
from django.test import Client


class TestClient(Client):

    def post(self, *args, **kwargs):
        if 'json' in kwargs:
            kwargs['data'] = json.dumps(kwargs['json'])
            kwargs['content_type'] = 'application/JSON'
            del kwargs['json']
        return super().post(*args, **kwargs)

    @property
    def is_authenticated(self):
        user = auth.get_user(self)
        return user.is_authenticated
