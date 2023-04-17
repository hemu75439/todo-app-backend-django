from django.db import models

# Create your models here.
class User(models.Model):
    _id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=300)

class Tasks(models.Model):
    _id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=254)
    description = models.CharField(max_length=1500)
    imagePath = models.CharField(max_length=500)
    creator = models.CharField(max_length=100)



