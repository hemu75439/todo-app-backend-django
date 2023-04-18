from django.db import models
import uuid

# Create your models here.
class User(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=300)

class Tasks(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    title = models.CharField(max_length=254)
    description = models.CharField(max_length=1500)
    imagePath = models.CharField(max_length=500)
    creator = models.CharField(max_length=100)



