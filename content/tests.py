from django.test import TestCase
from .models import Comment, Post, Follow, Like, Profile
from django.contrib.auth.models import User

# Create your tests here.
user = User.objects.get(id=1)

# class TestFollowers(TestCase):
#     def setUp(self):
#         self.new_user=User(first_name='Ray', last_name='Ray', username='Ray', email='ray@gmail.com',password='123')
#         self.new_user.save()
        # user=Follow(user_followers='lulu',following=1)
        # user.save()

#     def test_instance(self):
#         self.assertTrue(isinstance(self.new_user, Follow))

# class TestComment(TestCase):
#     def setUp(self):
#         self.new_user=User(first_name='Ray', last_name='Ray', username='Ray', email='ray@gmail.com',password='123')
#         self.new_user.save()
#         self.new_comment=Comment(comment='comment', author=self.new_user, post=self.new_post)
#         self.new_comment.save()

# class TestLike(TestCase):
#     def setUp(self):
#         self.new_user=User(first_name='Ray', last_name='Ray', username='Ray', email='ray@gmail.com',password='123')
#         self.new_user.save()
#         user=Like(author=1, post=1)
#         user.save()

#     def test_instance(self):
#         self.assertTrue(isinstance(self.new_user,Like))

class TestPost(TestCase):
    def setUp(self):
        # self.new_user=User(first_name='Ray', last_name='Ray', username='Ray', email='ray@gmail.com',password='123')
        # self.new_user.save()
        # self.profile=Profile(user=self.new_user, bio='testing', profile_pic='profile.jpg')
        
        self.new_post=Post(image = "default.jpg", name="Title", caption='testing', author=user)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_post,Post))

    def test_save_image(self):
        new_p=self.new_post
        new_p.save_image()
        posts=Post.get_posts()
        self.assertTrue(len(posts)>0)


    # def test_delete_image(self):
    #     new_p=self.new_post
    #     new_p.delete_image()
    #     posts=Post.objects.all()
    #     self.assertTrue(len(posts) < 1)

class TestUserProfile(TestCase):
    def setUp(self):
        self.new_user=User(first_name='Ray', last_name='Ray', username='Ray', email='Ray@gmail.com',password='123')
        self.new_user.save()

        self.profile=Profile(user=self.new_user, bio='testing', profile_pic='profile.jpg')

    def test_instance(self):
        self.assertTrue(isinstance(self.profile,Profile))

    
