from django.http import HttpResponseServerError, QueryDict
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.models import Tasks
from api.serielizers import TasksSerielizer
from django.core import serializers
from django.core.files.storage import default_storage
import json
import re
from todo_app_backend.settings import MEDIA_ROOT

@api_view(['GET'])
def getTask(request):
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
        return HttpResponseServerError({
            'status': {
                'code': 400,
                'message': 'Internal Server Error!'
            },
        })


@api_view(['POST'])
def addTask(req):
    try:
        file = req.data.get('image')
        extension = file.content_type.split('/').pop()
        file_name = re.sub(re.compile(r'\s+'), '', file.name) + '.' + extension
        save_file = default_storage.save(file_name, file)
        host = 'http://127.0.0.1:8000/' + 'api/images/'
        tasks_serielised = TasksSerielizer(data={
            'title': req.data.get('title'),
            'description': req.data.get('description'),
            'imagePath': host + file_name,
            'creator': '643d7301aa0f56e3ba79d4f5'
        })
        if tasks_serielised.is_valid():
            tasks_serielised.save()
        res = {
            'status': {
                'code': 200,
                'message': 'success'
            },
            'data': [],
        }
        return Response(res)
        
    except:
        return HttpResponseServerError({
            'status': {
                'code': 400,
                'message': 'Internal Server Error!'
            }, 
        })
