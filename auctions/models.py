from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField(max_length=64, unique=True)
    password = models.CharField(max_length=64)


class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    bid = models.FloatField(blank=True, default=0)
    image = models.CharField(max_length=64, blank=True)
    category = models.CharField(max_length=16, blank=True)

    def __str__(self):
        return f"{self.title}"
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist", default=1)
    listing = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="watchlist")