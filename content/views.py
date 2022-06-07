from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from instagram import settings
from .forms import UpdateUserForm, UpdateProfileForm, AddPostForm
from django.contrib.auth.decorators import login_required
from .models import Follow, Like, Post, Profile, Comment

# Create your views here.

def login(request):
  if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)     

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Username Does Not Exist! Choose Another One')
            return redirect('Login')

        if user is None:
            messages.error(request, 'Username/Password Is Incorrect or Account Is Not Activated!! Please Try Again')
            return redirect('Login')

        if user is not None:
            login(request, user)
            return redirect(reverse('index'))
  return render (request, 'login.html')
  
@login_required(login_url='login')
def index (request):
   posts = Post.objects.order_by('-created').all()
   profiles = Profile.objects.all()
   return render(request, 'index.html', {'posts':posts, 'profiles':profiles})

  

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
            messages.error(request, 'Passwords Do Not Match! Try Again')
            return redirect('Register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username Already Exists! Choose Another One')
            return redirect('Register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email Address Already Exists! Choose Another One')
            return redirect('Register')

        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email)
        user.set_password(password1)
        user.is_active = False
        user.save()        
  return render(request, 'register.html')
@login_required(login_url='login')
def Userprofile(request, username):
  current_user = request.user
  profile = User.objects.get(username=username)
  profile_details = Profile.objects.get(user = profile.id)
  images = Post.objects.filter(author = profile.id).all()
  images_count = Post.objects.filter(author = profile.id)
  followers = Profile.get_followers(self=profile)
  following = Profile.get_following(self=profile)
  is_followed = False
  if followers.filter(user_id=current_user.id).exists() or following.filter(user_id=current_user.id).exists():
      is_followed=True
  else:
      is_followed=False
  return render(request, 'User profile.html', {'profile':profile, 'profile_details':profile_details, 'images':images, 'images_count':images_count, 'followers':followers, 'following':following, 'current_user':current_user, 'is_followed':is_followed})

@login_required(login_url='Login')
def MyProfile(request, username):
    profile = User.objects.get(username=username)
    profile_details = Profile.objects.get(user = profile.id)
    images = Post.objects.filter(author = profile.id).all()
    images_count = Post.objects.filter(author = profile.id)
    followers = Profile.get_followers(self=profile)
    following = Profile.get_following(self=profile)
    return render(request, 'My profile.html', {'profile':profile, 'profile_details':profile_details, 'images':images, 'images_count':images_count, 'followers':followers, 'following':following})

@login_required(login_url='Login')
def EditProfile(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, '✅ Your Profile Has Been Updated Successfully!')
            return redirect('MyProfile', username=username)
        else:
            messages.error(request, "⚠️ Your Profile Wasn't Updated!")
            return redirect('EditProfile', username=username)
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'Edit Profile.html', {'user_form': user_form, 'profile_form': profile_form})
  

@login_required(login_url='Login')
def Logout(request):
    logout(request)
    messages.success(request, 'Successfully Logged Out!')
    return redirect(reverse('Login'))
