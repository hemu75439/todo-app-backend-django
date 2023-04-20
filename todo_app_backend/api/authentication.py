
from django.http import HttpResponseForbidden
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import authentication
import json
import jwt

class ApiAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        if not 'Authorization' in request.headers:
            return (None, '')

        token = request.headers['Authorization']
        token = token.split()[1]
        try:
            decoded_token = jwt.decode(token, "secret", algorithms=["HS256"])
            return (decoded_token, '')
        except:
            return (None, '')
        