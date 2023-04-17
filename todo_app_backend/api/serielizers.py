from rest_framework import serializers

from api.models import User, Tasks


class UserSerielizer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('_id', 'email', 'password')

class TasksSerielizer(serializers.ModelSerializer):
    class Meta:
        model=Tasks
        fields='__all__'