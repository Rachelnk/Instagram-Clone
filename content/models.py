from tkinter import CASCADE
from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.

class Profile(models.Model):
    profile_pic = CloudinaryField('')
    bio = models.TextField()
    username = models.CharField(max_length=60)

class Post(models.Model):
  image = CloudinaryField('image')
  name = models.CharField(max_length=60)
  caption = models.TextField()
  comments = models.TextField()
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
  created = models.DateTimeField(auto_now_add=True, null=True)
  # likes = 

class Comment(models.Model):
  comment = models.TextField()
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
  user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
  created = models.DateTimeField(auto_now_add=True, null=True)




