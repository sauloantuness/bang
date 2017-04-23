from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from home.models import Profile, Solution
from django.contrib.auth.models import User
from functools import reduce
# Create your views here.

@login_required
def ranking(request, order='score'):
    profiles = []

    for p in Profile.objects.all():
        profile = {
            'profile': p,
            'name': p.name,
            'uri': Solution.objects.filter(problem__judge='uri', profile=p).count(),
            'uva': Solution.objects.filter(problem__judge='uva', profile=p).count(),
            'spoj': Solution.objects.filter(problem__judge='spoj', profile=p).count(),
            'total': 0,
            'score': 0,
        }
        profile['total'] = profile['uri'] + profile['uva'] + profile['spoj']
        profile['score'] = reduce(lambda acc, s: s.problem.level + acc, p.solution_set.all(), 0)
        profiles.append(profile)

    context = {
        'profiles' : sorted(profiles, key=lambda k: k[order], reverse=(order != 'name'))
    }

    return render(request, 'ranking/ranking.html', context)