from . import views
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('login', views.loginUser, name= 'login'),
  path('', views.index, name = 'index' ),
  path('register/', views.register, name = 'register'),
  re_path(r'^profile/(?P<username>\w{0,50})/$', views.MyProfile, name = 'my_profile'),
  re_path(r'^user/(?P<username>\w{0,50})/$', views.user_profile, name="user_profile"),
  re_path(r'^profile/(?P<username>\w{0,50})/edit/$', views.EditProfile, name="EditProfile"),
  re_path(r'^profile/(?P<username>\w{0,50})/settings/$', views.Settings, name="Settings"),
  # re_path(r'^post/<id>(\d+)', views.SingleImage, name="SingleImage"),
  re_path(r'^profile/(?P<username>\w{0,50})/image/add/$', views.add_post, name="add_post"),
  re_path(r'^post/<id>(\d+)/like/$', views.PostLike, name="PostLike"),
  path('logout/', views.Logoutuser, name="logout"),
  re_path(r'^follow/user/(?P<username>\w{0,50})/$', views.FollowUser, name="FollowUser"),
  re_path(r'^post/<id>(\d+)/comment/$', views.AddComment, name="AddComment"),
  re_path(r'^search-results/$', views.Search, name="search_results")

]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
