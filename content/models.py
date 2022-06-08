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
    updated = models.DateTimeField(auto_now=True, verbose_name='Date Updated')

    def save_profile(self):
        self.user

    def delete_profile(self):
        self.delete()

    @classmethod
    def search_profile(cls, name):
        return cls.objects.filter(user__username__icontains=name).all()
    
    def get_posts(self):
      return Post.objects.filter(user=self).all()

    # user followers
    def get_followers(self):
      return self.followers.all()

    def __str__(self):
      return str(self.user)

    # people user follows
    def get_following(self):
      return self.following.all()

    class Meta: 
      verbose_name_plural = 'Profiles'

# post class model
class Post(models.Model):
  image = CloudinaryField('image')
  name = models.CharField(max_length=60)
  caption = models.TextField()
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
  author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
  created = models.DateTimeField(auto_now_add=True, null=True)
  updated = models.DateTimeField(auto_now=True, verbose_name='Date Updated')

  def get_posts(self):
    posts = Post.objects.filter(user=self).all()
    return posts

  def save_image(self):
    self.save()
  
  def get_likes(self):
    likes = Like.objects.filter(post=self)
    return len(likes)

  def get_comments(self):
    comments = Comment.objects.filter(post=self)
    return comments

  def delete_image(self):
    self.delete()

  def __str__(self):
    return str(self.name)

  class Meta:
    ordering = ['created']
 

class Comment(models.Model):
  comment = models.TextField(max_length=1000)
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  created = models.DateTimeField(auto_now_add=True, null=True)

  def display_comment(self,post_id):
        comments = Comment.objects.filter(self = post_id)
        return comments

  def __str__(self):
       return str(self.comment)

  class Meta:
      ordering = ['-pk']

class Like(models.Model):
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  post = models.ForeignKey(Post,on_delete=models.CASCADE)

class Follow(models.Model):
  user_followers = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'following')
  following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

  def __str__(self):
    return str(self.user_followers)




