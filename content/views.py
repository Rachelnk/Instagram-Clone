from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def login(request):
  return render (request, 'login.html')

def index (request):
  return render (request, 'index.html')

