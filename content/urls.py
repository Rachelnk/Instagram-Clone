from . import views
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('login', views.loginUser, name= 'login'),
  path('', views.index, name = 'index' ),
  path('register', views.register, name = 'register'),
  path('profile/<str:username>', views.MyProfile, name = 'MyProfile'),
  path('user/<str:username>', views.UserProfile, name="user_profile"),
    path('profile/<str:username>/edit', views.EditProfile, name="EditProfile"),
    path('profile/<str:username>/settings', views.Settings, name="Settings"),
    path('post/<int:id>', views.SingleImage, name="SingleImage"),
    path('profile/<str:username>/image/add', views.AddNewPost, name="AddNewPost"),
    path('post/<int:id>/like', views.PostLike, name="PostLike"),
    path('logout', views.Logout, name="logout"),
    path('follow/user/<str:username>', views.FollowUser, name="FollowUser"),
    path('post/<int:id>/comment', views.AddComment, name="AddComment"),
    path('search-results', views.Search, name="search_results")

]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
