from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from instagram import settings
from .forms import UpdateUserForm, UpdateProfileForm, AddPostForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .models import Follow, Like, Post, Profile, Comment
from django.contrib.auth import update_session_auth_hash

# Create your views here.

def loginUser(request):
  if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)     

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Username Does Not Exist! Choose Another One')
            return redirect('login')

        if user is None:
            messages.error(request, 'Username/Password Is Incorrect!! Please Try Again')
            return redirect('login')

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
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username Already Exists! Choose Another One')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email Address Already Exists! Choose Another One')
            return redirect('register')

        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email)
        user.set_password(password1)
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
  return render(request, 'user_profile.html', {'profile':profile, 'profile_details':profile_details, 'images':images, 'images_count':images_count, 'followers':followers, 'following':following, 'current_user':current_user, 'is_followed':is_followed})

@login_required(login_url='login')
def MyProfile(request, username):
    profile = User.objects.get(username=username)
    profile_details = Profile.objects.get(user = profile.id)
    images = Post.objects.filter(author = profile.id).all()
    images_count = Post.objects.filter(author = profile.id)
    followers = Profile.get_followers(self=profile)
    following = Profile.get_following(self=profile)
    return render(request, 'my_profile.html', {'profile':profile, 'profile_details':profile_details, 'images':images, 'images_count':images_count, 'followers':followers, 'following':following})

@login_required(login_url='Login')
def EditProfile(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your Profile Has Been Updated Successfully!')
            return redirect('my_profile', username=username)
        else:
            messages.error(request, "Your profile Wasn't Updated!")
            return redirect('EditProfile', username=username)
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})
@login_required(login_url='login')
def user_profile(request, username):
    current_user = request.user
    profile = User.objects.get(username=username)
    profile_details = Profile.objects.get(user = profile.id)
    images = Post.objects.filter(author = profile.id).all()
    images_count = Post.objects.filter(author = profile.id)
    followers = Profile.get_followers(self=profile)
    following = Profile.get_following(self=profile)
    is_followed = False
    if followers.filter(id=current_user.id).exists() or following.filter(id=current_user.id).exists():
        is_followed=True
    else:
        is_followed=False
    return render(request, 'user_profile.html', {'profile':profile, 'profile_details':profile_details, 'images':images, 'images_count':images_count, 'followers':followers, 'following':following, 'current_user':current_user, 'is_followed':is_followed})
  

@login_required(login_url='login')
def Logoutuser(request):
    logout(request)
    messages.success(request, 'Successfully Logged Out!')
    return redirect(reverse('login'))

# def SingleImage(request, id):
#     post = Post.objects.get(id = id)
#     print(post)
#     likes = Like.objects.filter(post = post.id).count()
#     print(likes)
#     comments = Comment.objects.filter(post = post.id).count()
#     print(comments)
    
#     return render(request,'index.html', {'post': post, 'comments':comments, 'likes':likes})

@login_required(login_url='login')
def add_post(request, username):
    form = AddPostForm()
    if request.method == "POST":
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.profile = request.user.profile
            post.save()
            messages.success(request, 'Your Post Was Created Successfully!')
            return redirect('my_profile', username=username)
        else:
            messages.error(request, "Your Post Wasn't Created!")
            return redirect('add_post', username=username)
    else:
        form = AddPostForm()
    return render(request, 'add_post.html', {'form':form})

def Search(request):
    current_user = request.user
    if request.method == 'POST':
        search = request.POST['imageSearch']
        users = User.objects.filter(username__icontains = search).all()
        if not users:
            return render(request, 'search_results.html', {'search':search, 'users':users})
        else:
            images = Post.objects.filter(author = users[0]).all()
            images_count = Post.objects.filter(author = users[0])
            follower_count = Follow.objects.filter(following = users[0])
            following_count = Follow.objects.filter(user_followers = users[0])
            is_followed = False
            if follower_count.filter(id=current_user.id).exists() or following_count.filter(id=current_user.id).exists():
                is_followed=True
            else:
                is_followed=False
            return render(request, 'search_results.html', {'search':search, 'users':users, 'images':images, 'images_count':images_count, 'follower_count':follower_count, 'following_count':following_count, 'current_user':current_user, 'is_followed':is_followed})
    else:
        return render(request, 'search_results.html')
@login_required(login_url='login')
def AddComment(request, id):
    post = Post.objects.get(id=id)
    if request.method == "POST":
        usercomment = request.POST['comment']
        comment_obj = Comment.objects.create(comment = usercomment, author = request.user, post = post)
        comment_obj.save()
        messages.success(request, 'Your Comment Was Created Successfully!')
        return redirect('index')
    else:
        messages.error(request, "Your Comment Wasn't Created!")
        return redirect('index')

@login_required(login_url='login')
def PostLike(request,id):
    postTobeliked = Post.objects.get(id = id)
    currentUser = User.objects.get(id = request.user.id)
    if not postTobeliked:
        return "Post Not Found!"
    else:
        like = Like.objects.filter(author = currentUser, post = postTobeliked)
        if like:
            messages.error(request, 'You Can Only Like A Post Once!')
            return redirect('index')
        else:
            likeToadd = Like(author = currentUser, post = postTobeliked)
            likeToadd.save()
            messages.success(request, 'You Successfully Liked The Post!')
            return redirect('index')

@login_required(login_url='login')
def FollowUser(request, username):
    userTobefollowed = User.objects.get(username = username)
    currentUser = request.user
    is_followed = False
    if userTobefollowed.id == currentUser.id:
        messages.error(request, "You can't follow yourself!")
        return redirect('user_profile', username=username)
    if not userTobefollowed:
        messages.error(request, "User Does Not Exist!")
        return redirect('user_profile', username=username)
    else:
        follow = Follow.objects.filter(user_followers = currentUser, following = userTobefollowed)
        if follow:
            messages.error(request, 'You Can Only Follow A User Once!')
            return redirect('user_profile', username=username)
        else:
            folowerToadd = Follow(user_followers = currentUser, following = userTobefollowed)
            folowerToadd.save()
            messages.success(request, "You Are Now Following This User!")
            return redirect('user_profile', username=username)

@login_required(login_url='login')
def Settings(request, username):
    username = User.objects.get(username=username)
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your Password Has Been Updated Successfully!')
            return redirect("my_profile", username=username)
        else:
            messages.error(request, "Your Password Wasn't Updated!")
            return redirect("Settings", username=username)
    else:
        form = PasswordChangeForm(data=request.POST, user=request.user)
        return render(request, "Settings.html", {'form': form})