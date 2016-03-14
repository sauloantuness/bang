from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout

# Create your views here.

def login(request):
	return render(request, 'home/login.html')

def logout(request):
	auth_logout(request)
	return redirect('/login/')


def home(request):
	return render(request, 'home/home.html')
