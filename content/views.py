from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from instagram import settings
from .forms import UpdateUserForm, UpdateProfileForm, AddPostForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def login(request):
  return render (request, 'login.html')
  
@login_required(login_url='login')
def index (request):
  return render (request, 'index.html')

def register(request):

  if request.method == 'POST':
        context = {'has_error': False}
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, '⚠️ Passwords Do Not Match! Try Again')
            return redirect('Register')

        if User.objects.filter(username=username).exists():
            messages.error(request, '⚠️ Username Already Exists! Choose Another One')
            return redirect('Register')

        if User.objects.filter(email=email).exists():
            messages.error(request, '⚠️ Email Address Already Exists! Choose Another One')
            return redirect('Register')

        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email)
        user.set_password(password1)
        user.is_active = False
        user.save()

        
  return render(request, 'register.html')

def profile(request):
  return render(request,'profile.html')

