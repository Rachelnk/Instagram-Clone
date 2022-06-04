from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User', null=True)
    profile_pic = CloudinaryField('')
    bio = models.TextField()
    username = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Date Created, ', null=True)
    
    def get_posts(self):
      return Post.objects.filter(user=self).all()

    # user followers
    def get_followers(self):
      return self.followers.all()

    # people user follows
    def get_following(self):
      return self.following.all()



class Post(models.Model):
  image = CloudinaryField('image')
  name = models.CharField(max_length=60)
  caption = models.TextField()
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
  author= models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
  created = models.DateTimeField(auto_now_add=True, null=True)
  # likes = 

class Comment(models.Model):
  comment = models.TextField(max_length=1000)
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  created = models.DateTimeField(auto_now_add=True, null=True)

class Like(models.Model):
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  post = models.ForeignKey(Post,on_delete=models.CASCADE)
class Follow(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'Following')
  following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)




