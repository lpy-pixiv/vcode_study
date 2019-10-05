from django.db import models


# Create your models here.
class User(models.Model):

    username = models.CharField(max_length=18)

    password = models.CharField(max_length=50)

    create_time = models.DateTimeField(auto_now_add=True)
