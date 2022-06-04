from . import views
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('', views.login, name= 'home'),
  path('login/', views.index, name = 'login' ),
  path('register/', views.register, name = 'register'),
  path('profile/', views.profile, name = 'profile')

]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
