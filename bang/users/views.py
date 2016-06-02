from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from home.models import *
# Create your views here.

@login_required
def users(request):
	profiles = []
	for p in Profile.objects.all().order_by('name'):
		profiles.append({
				'profile' : p,
				'solutions' : Solution.objects.filter(profile=p).count()
			})

	context = {
		'profiles' : profiles,
	}

	return render(request, 'users/users.html', context)

def historic(profile_id):
	now = datetime.now().date()
	begin = now - timedelta(days=7)

	days = [begin + timedelta(days=x) for x in range(1, 8)]

	problems_solved = []
	for day in days:
		problems_solved.append(Solution.objects.filter(profile__id=profile_id, date__range=[day, day + timedelta(days=1)]).count())

	days = [ d.strftime('%d/%m') for d in days]
	
	return {
		'problems_solved' : problems_solved,
		'days' : days,
	}

def uri(profile_id):
	return Solution.objects.filter(problem__judge='uri', profile__id=profile_id).order_by('problem__code')

def uva(profile_id):
	return Solution.objects.filter(problem__judge='uva', profile__id=profile_id).order_by('problem__code')

def spoj(profile_id):
	return Solution.objects.filter(problem__judge='spoj', profile__id=profile_id).order_by('problem__code')

@login_required
def profile(request, profile_id):
	context = {
		'profile' : Profile.objects.get(id=profile_id),
		'solutions' : {
			'uri' : Solution.objects.filter(profile__id=profile_id, problem__judge='uri').count(),
			'uva' : Solution.objects.filter(profile__id=profile_id, problem__judge='uva').count(),
			'spoj' : Solution.objects.filter(profile__id=profile_id, problem__judge='spoj').count(),
		},
		'recentlySolved' : Solution.objects.filter(profile__id=profile_id).order_by('-date')[:5],
		'historic' : historic(profile_id),
		'uri' : uri(profile_id),
		'uva' : uva(profile_id),
		'spoj' : spoj(profile_id),
		'teams' : Profile.objects.get(id=profile_id).teams.all(),
	}

	return render(request, 'users/user.html', context)