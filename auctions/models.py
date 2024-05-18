from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField(max_length=64, unique=True)
    password = models.CharField(max_length=64)

class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    price = models.FloatField()