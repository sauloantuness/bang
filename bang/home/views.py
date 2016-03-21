from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Solution

# Create your views here.

def login(request):
	return render(request, 'home/login.html')

def logout(request):
	auth_logout(request)
	return redirect('/login/')

def group():
	return {
		'uri' : 150,
		'uva' : 0,
		'spoj' : 0,
	}

def recentlySolved():
	return Solution.objects.all().order_by('-date')[:5]

	return [
		{
			'name' : 'Saulo Antunes',
			'profileId' : 1,
			'problem' : 'URI 1001 - Extremely Basic',
			'problemId' : 2,
			'date' : '1 day ago'
		},
		{
			'name' : 'Saulo Antunes',
			'profileId' : 1,
			'problem' : 'URI 1001 - Extremely Basic',
			'problemId' : 2,
			'date' : '1 day ago'
		},
	]

def historic():
	return {
		'problems_solved' : [6, 6, 6, 6, 5, 5, 10],
		'days' : ['12/02', '13/02', '14/02', '15/02', '16/02', '17/02', '18/02'],
	}

def trends():
	return [
		{
			'name' : 'Saulo Antunes',
			'profileId' : 1
		},
	]

def events():
	return [
		{
			'date' : '01/09/1991',
			'description' : 'lorem ipsum'	
		},
	]


@login_required
def home(request):
	if request.user.is_superuser:
		auth_logout(request)
		return redirect('/login/')

	context = {
		'group' : group(),
		'recentlySolved' : recentlySolved(),
		'historic' : historic(),
		'trends' : trends(),
		'events' : events()
	}

	return render(request, 'home/home.html', context)