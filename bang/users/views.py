from django.shortcuts import render
from home.models import Profile, Solution
from datetime import datetime, timedelta
# Create your views here.

def users(request):
	profiles = Profile.objects.all().order_by('name')
	users = []
	for p in profiles:
		users.append({
				'profile' : p,
				'solutions' : Solution.objects.filter(profile=p).count()
			})

	context = {
		'users' : users,
	}

	return render(request, 'users/users.html', context)

def historic(user_id):
	now = datetime.now()
	begin = now - timedelta(days=7)

	days = [begin + timedelta(days=x) for x in range(1, 8)]

	problems_solved = []
	for day in days:
		problems_solved.append(Solution.objects.filter(profile__user__id=user_id, date__range=[day, day + timedelta(days=1)]).count())

	days = [ d.strftime('%d/%m') for d in days]
	
	return {
		'problems_solved' : problems_solved,
		'days' : days,
	}

def uri(user_id):
	return Solution.objects.filter(problem__judge='uri', profile__user__id=user_id).order_by('problem__code')

def uva(user_id):
	return Solution.objects.filter(problem__judge='uva', profile__user__id=user_id).order_by('problem__code')

def spoj(user_id):
	return Solution.objects.filter(problem__judge='spoj', profile__user__id=user_id).order_by('problem__code')

def user(request, user_id):
	context = {
		'profile' : Profile.objects.get(user__id=user_id),
		'solutions' : {
			'uri' : Solution.objects.filter(profile__user__id=user_id, problem__judge='uri').count(),
			'uva' : Solution.objects.filter(profile__user__id=user_id, problem__judge='uva').count(),
			'spoj' : Solution.objects.filter(profile__user__id=user_id, problem__judge='spoj').count(),
		},
		'recentlySolved' : Solution.objects.filter(profile__user__id=user_id).order_by('-date')[:5],
		'historic' : historic(user_id),
		'uri' : uri(user_id),
		'uva' : uva(user_id),
		'spoj' : spoj(user_id),
	}

	return render(request, 'users/user.html', context)