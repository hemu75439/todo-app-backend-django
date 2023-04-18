from django.http import HttpResponseServerError, HttpResponseBadRequest
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from api.models import User
from api.serielizers import UserSerielizer
from django.core import serializers
import json
from datetime import timedelta
from rest_framework_simplejwt.tokens import Token, AccessToken

@api_view(['POST'])
@authentication_classes([])
def signup(req):
    try:
        user_serielised = UserSerielizer(data={
            'email': req.data.get('email'),
            'password': req.data.get('password')
        })
        print(user_serielised.is_valid())
        if user_serielised.is_valid():
            user_serielised.save()
        res = {
            'status': {
                'code': 200,
                'message': 'Signup successful!'
            },
        }
        return Response(res)
        
    except:
        return HttpResponseServerError(json.dumps({
            'status': {
                'code': 500,
                'message': 'Internal Server Error!'
            }, 
        }), content_type="application/json")
    



@api_view(['POST'])
@authentication_classes([])
def login(req):
    try:
        user_from_db = User.objects.filter(email=req.data.get('email'))
        if not len(user_from_db):
            return HttpResponseBadRequest(json.dumps({
                        'status': {
                            'code': 400,
                            'message': 'User not found!'
                        }, 
                    }), content_type="application/json")
        
        user_json = serializers.serialize('json', user_from_db)
        user_json = json.loads(user_json)
        print(user_json)
        user = {
            '_id': user_json[0]['pk'],
            'email': user_json[0]['fields']['email'],
            'password': user_json[0]['fields']['password'],
        }

        # Use bcrypt compare instead
        if not user['password'] == req.data.get('password'):
            return HttpResponseBadRequest(json.dumps({
                        'status': {
                            'code': 400,
                            'message': 'Invalid Credentials!'
                        }, 
                    }), content_type="application/json")
        
        print('from db ::\n', user)
        # token = Token.for_user(user)
        token = "abcd"
        res = {
            'status': {
                'code': 200,
                'message': 'Login successful!'
            },
            'data': {
                'expiresIn': timedelta(minutes=60),
                'token': str(token),
                'userId': user['_id']
            }
        }
        return Response(res)
        
    except:
        return HttpResponseServerError(json.dumps({
            'status': {
                'code': 500,
                'message': 'Internal Server Error!'
            }, 
        }), content_type="application/json")
