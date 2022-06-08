from django.test import TestCase
from .models import Comment, Post, Follow, Like, Profile
from django.contrib.auth.models import User

# Create your tests here.
user = User.objects.get(id=1)

class TestFollowers(TestCase):
    def setUp(self):
        self.new_user=User(first_name='Ray', last_name='Ray', username='Ray', email='ray@gmail.com',password='123')
        self.new_user.save()
        user=Follow(user='user',following=1)
        user.save()

    def test_instance(self):
        self.assertTrue(isinstance(user, Follow))

class TestComment(TestCase):
    def setUp(self):
        self.new_comment=Comment(comment='comment', author=user, post=self.new_post)
        self.new_comment.save()
