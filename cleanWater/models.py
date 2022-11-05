from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from django.forms import DateField

# Create your models here.
class User(User):
    pass
class Comment(models.Model):
    comment = models.IntegerField(default=0)

class UserProfile(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    address = models.CharField(verbose_name="Address", max_length=100, null=True, blank=True)
    town = models.CharField(verbose_name="Town/City", max_length=100, null=True, blank=True)
    county = models.CharField(verbose_name="County", max_length=100, null=True, blank=True)
    post_code = models.CharField(verbose_name="Post Code", max_length=8, null=True, blank=True)
    country = models.CharField(verbose_name="Country", max_length=100, null=True, blank=True)
    longitude = models.CharField(verbose_name="Longitude", max_length=50, null=True, blank=True)
    latitude = models.CharField(verbose_name="Latitude", max_length=50, null=True, blank=True)
    
    has_profile = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    
    def __str__(self):
        return f'{self.user}'
    
class Articles(models.Model):
    title = models.CharField(max_length=100)
    image = models.CharField(max_length=1000)
    briefDesc = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-date"]
        
