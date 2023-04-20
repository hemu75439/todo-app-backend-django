from django.http import HttpResponseServerError
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from api.models import Tasks
from api.serielizers import TasksSerielizer
from django.core import serializers
from django.core.files.storage import default_storage
import json
import re
from api.authentication import ApiAuthentication

@api_view(['GET'])
def getTasks(request):
    try:
        tasks_from_db = Tasks.objects.all()
        tasks_json = serializers.serialize('json', list(tasks_from_db))
        tasks_json = json.loads(tasks_json)
        tasks = []
        for t in tasks_json:
            task = {
                '_id': t['pk'],
                'title': t['fields']['title'],
                'description': t['fields']['description'],
                'imagePath': t['fields']['imagePath'],
                'creator': t['fields']['creator'],
            }
            tasks.append(task)
        res = {
            'status': {
                'code': 200,
                'message': 'success'
            },
            'data': tasks,
            'totalCount': len(tasks)
        }
        return Response(res)
    except:
        return HttpResponseServerError(json.dumps({
            'status': {
                'code': 500,
                'message': 'Internal Server Error!'
            }, 
        }), content_type="application/json")
    

@api_view(['GET'])
@authentication_classes([ApiAuthentication])
def getTask(request, id):
    try:
        if(request.user is None):
            return HttpResponseServerError(json.dumps({
            'status': {
                'code': 403,
                'message': 'Unauthorised!'
            }, 
        }), content_type="application/json")
        tasks_from_db = Tasks.objects.filter(pk=id)
        tasks_json = serializers.serialize('json', list(tasks_from_db))
        tasks_json = json.loads(tasks_json)
        res = {
            'status': {
                'code': 200,
                'message': 'success'
            },
            'data': {
                '_id': tasks_json[0]['pk'],
                'title': tasks_json[0]['fields']['title'],
                'description': tasks_json[0]['fields']['description'],
                'imagePath': tasks_json[0]['fields']['imagePath'],
                'creator': tasks_json[0]['fields']['creator'],
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



@api_view(['POST'])
@authentication_classes([ApiAuthentication])
def addTask(req):
    try:
        if(req.user is None):
            return HttpResponseServerError(json.dumps({
            'status': {
                'code': 403,
                'message': 'Unauthorised!'
            }, 
        }), content_type="application/json")
        file = req.data.get('image')
        extension = file.content_type.split('/').pop()
        file_name = re.sub(re.compile(r'\s+'), '', file.name) + '.' + extension
        save_file = default_storage.save(file_name, file)
        host = req.scheme + '://' + req.get_host() + '/api/images/'
        tasks_serielised = TasksSerielizer(data={
            'title': req.data.get('title'),
            'description': req.data.get('description'),
            'imagePath': host + save_file,
            'creator': req.data.get('userId')
        })
        if tasks_serielised.is_valid():
            tasks_serielised.save()
        res = {
            'status': {
                'code': 200,
                'message': 'Created successfully!'
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



@api_view(['PATCH'])
@authentication_classes([ApiAuthentication])
def updateTask(req, id):
    try:
        if(req.user is None):
            return HttpResponseServerError(json.dumps({
            'status': {
                'code': 403,
                'message': 'Unauthorised!'
            }, 
        }), content_type="application/json")
        imagePath = None
        if req.data.get('imagePath'):
            imagePath = req.data.get('imagePath')
        else:
            file = req.data.get('image')
            extension = file.content_type.split('/').pop()
            file_name = re.sub(re.compile(r'\s+'), '', file.name) + '.' + extension
            save_file = default_storage.save(file_name, file)
            host = req.scheme + '://' + req.get_host() + '/api/images/'
            imagePath = host + save_file

        Tasks.objects.filter(pk=id).update(
            title=req.data.get('title'),
            description=req.data.get('description'),
            imagePath=imagePath,
            creator=req.data.get('userId'),
        )
        res = {
            'status': {
                'code': 200,
                'message': 'Updated successfully!'
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
    


@api_view(['DELETE'])
@authentication_classes([ApiAuthentication])
def deleteTask(req, id):
    try:
        if(req.user is None):
            return HttpResponseServerError(json.dumps({
            'status': {
                'code': 403,
                'message': 'Unauthorised!'
            }, 
        }), content_type="application/json")
        Tasks.objects.filter(pk=id).delete()
        res = {
            'status': {
                'code': 200,
                'message': 'Deleted successfully!'
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