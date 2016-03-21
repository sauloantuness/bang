from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from .models import Profile, Solution
from datetime import datetime, timedelta

# Create your views here.

def login(request):
	return render(request, 'home/login.html')

def logout(request):
	auth_logout(request)
	return redirect('/login/')

def group():
	return {
		'uri' : Solution.objects.filter(problem__judge='uri').count(),
		'uva' : 0,
		'spoj' : 0,
	}

def recentlySolved():
	return Solution.objects.all().order_by('-date')[:5]

def historic(user):
	now = datetime.now()
	begin = now - timedelta(days=7)

	days = [begin + timedelta(days=x) for x in range(1, 8)]

	problems_solved = []
	for day in days:
		problems_solved.append(Solution.objects.filter(date__range=[day, day + timedelta(days=1)]).count())

	days = [ d.strftime('%d/%m') for d in days]
	
	return {
		'problems_solved' : problems_solved,
		'days' : days,
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
		'historic' : historic(request.user),
		'trends' : trends(),
		'events' : events()
	}

	return render(request, 'home/home.html', context)