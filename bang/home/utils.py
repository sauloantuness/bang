from django.db.models import Count
from datetime import datetime, timedelta
from home.models import *

def set_profile(backend, response, user, is_new=False, *args, **kwargs):
    if backend.name == 'facebook':
        try:
            p = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            p = Profile()
            p.user = user
        
        p.name = response['name']
        p.picture = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
        p.facebookId = response['id']
        p.save()

def getContests(orderBy='-date'):
	'''
	Return a list of contests order by the -date.
	'''
	contests = []

	for c in Contest.objects.all().order_by(orderBy):
		contest = {
			'contest'  : c,
			'num_profiles' : c.profiles.count(),
			'num_problems' : c.problems.count(),
		}

		contests.append(contest)

	return contests

def getSolutionsAmount(profile=None, team=None):
	'''
	Return the amount of distinct problems solved by group, team or user.
	'''
	return {
		'uri' : Solution.objects.filter(problem__judge='uri').distinct('problem').count(),
		'uva' : Solution.objects.filter(problem__judge='uva').distinct('problem').count(),
		'spoj' : 0,
	}

def getLastSolutions():
	'''
	Return a list with the last solutions.
	'''
	return Solution.objects.all().order_by('-date')[:10]

def getHistoric():
	'''
	Return a list of problems solved by day of the user, team or group.
	'''
	now = datetime.now().date()
	begin = now - timedelta(days=7)

	days = [begin + timedelta(days=x) for x in range(1, 8)]

	problems_solved = []
	for day in days:
		problems_solved.append(Solution.objects.filter(date__range=[day, day + timedelta(days=1)]).count())

	days = [d.strftime('%d/%m') for d in days]
	
	return {
		'problems_solved' : problems_solved,
		'days' : days,
	}

def getTrends():
	'''
	Return a list of profiles with more solutions in the last 7 days.
	'''
	d = datetime.now().date() - timedelta(days=7)

	return {
		'profiles' : Profile.objects.filter(solution__date__gt=d).annotate(num_solutions=Count('solution')).order_by('-num_solutions')[:5]
	}

def getEvents():
	return [
		{
			'date' : '04/06/2016',
			'description' : 'Maratona Mineira'	
		},
	]