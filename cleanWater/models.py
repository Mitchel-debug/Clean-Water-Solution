from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from django.forms import DateField

# Create your models here.
class User(User):
    pass
class Comment(models.Model):
    comment = models.IntegerField(default=0)

class Articles(models.Model):
    title = models.CharField(max_length=100)
    image = models.CharField(max_length=1000)
    briefDesc = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-date"]