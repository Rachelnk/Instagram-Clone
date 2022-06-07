from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

def login(request):
  return render (request, 'login.html')
  
@login_required(login_url='login')
def index (request):
  return render (request, 'index.html')

def register(request):
  return render(request, 'register.html')

def profile(request):
  return render(request,'profile.html')

