from django.db import models
from django.contrib.auth.models import AbstractUser	

class User(AbstractUser):
    username = models.CharField(max_length = 200, unique=True)
    password = models.CharField(max_length = 200)
    name = models.CharField(max_length = 200)
    birth = models.DateField('date published',null=True)
    gender = models.CharField(max_length = 10)
    phone = models.CharField(max_length = 200)
    digitalwallet = models.TextField()
    nftwallet = models.TextField()