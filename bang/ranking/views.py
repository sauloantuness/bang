from django.shortcuts import render
from home.models import Profile, Solution
# Create your views here.

def ranking(request, order='all'):
	context = {}
	profiles = []

	for p in Profile.objects.all():
		profile = {
			'name' : p.name,
			'id' : p.id,
			'uri' : Solution.objects.filter(problem__judge='uri', profile=p).count(),
			'uva' : Solution.objects.filter(problem__judge='uva', profile=p).count(),
			'spoj' : Solution.objects.filter(problem__judge='spoj', profile=p).count(),
			'contests' : 0,
			'all' : 0,
		}
		profile['all'] = profile['uri'] + profile['uva'] + profile['spoj']
		profiles.append(profile)

	context['profiles'] = sorted(profiles, key=lambda k: k[order], reverse=(order != 'name')) 

	return render(request, 'ranking/ranking.html', context)