from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.

class Image(models.Model):
  image = CloudinaryField('image')
  name = models.CharField(max_length=60)
  caption = models.TextField()
  comments = models.TextField()
  # likes = 

class Profile(models.Model):
    profile_pic = CloudinaryField('')
    bio = models.TextField()
    username = models.CharField(max_length=60)

