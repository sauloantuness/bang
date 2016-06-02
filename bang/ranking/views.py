from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from home.models import Profile, Solution
from django.contrib.auth.models import User
# Create your views here.

@login_required
def ranking(request, order='all'):
	profiles = []

	for p in Profile.objects.all():
		profile = {
			'profile' : p,
			'uri'  : Solution.objects.filter(problem__judge='uri', profile=p).count(),
			'uva'  : Solution.objects.filter(problem__judge='uva', profile=p).count(),
			'spoj' : Solution.objects.filter(problem__judge='spoj', profile=p).count(),
			'contests' : 0,
			'all' : 0,
		}
		profile['all'] = profile['uri'] + profile['uva'] + profile['spoj']
		profiles.append(profile)

	context = {
		'profiles' : sorted(profiles, key=lambda k: k[order], reverse=(order != 'name'))
	}

	return render(request, 'ranking/ranking.html', context)