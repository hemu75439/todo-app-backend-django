from rest_framework import serializers

from api.models import User, Tasks


class UserSerielizer(serializers.ModelSerializer):
    class Meta:
        model=User
        feilds=('_id', 'email', 'password')

class TasksSerielizer(serializers.ModelSerializer):
    class Meta:
        model=Tasks
        feilds=('_id', 'title', 'description', 'imagePath', 'creator')