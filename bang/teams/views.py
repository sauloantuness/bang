from django.shortcuts import render, redirect
from home.models import Profile, Team, Invite, Solution
from django.contrib.auth.decorators import login_required

def teamsInvite(request, answer, invite_id):
	invite = Invite.objects.get(id=invite_id)
	profile = invite.profile
	team = invite.team
	if answer == 'yes':
		team.profiles.add(profile)

	invite.delete()

	return redirect('/settings')


def teamsDelete(request, team_id):
	team = Team.objects.get(id=team_id)
	team.delete()
	return redirect('/settings')


def teamsLeave(request, team_id):
	team = Team.objects.get(id=team_id)
	profile = Profile.objects.get(user=request.user)
	team.profiles.remove(profile)
	return redirect('/settings')


@login_required
def teams(request):
	context = {
		'teams' : Team.objects.all(),
	}

	return render(request, 'teams/teams.html', context)


@login_required
def team(request, team_id):
	team = Team.objects.get(id=team_id)
	context = {
		'team' : team,
		'solutions' : {
			'uri' : Solution.objects.filter(profile__in=team.profiles.all(), problem__judge='uri').distinct("problem__code").count(),
			'uva' : Solution.objects.filter(profile__in=team.profiles.all(), problem__judge='uva').distinct("problem__code").count(),
			'spoj' : Solution.objects.filter(profile__in=team.profiles.all(), problem__judge='spoj').distinct("problem__code").count(),
		},
		'skills' : team.getSkills(),
		'recentlySolved' : Solution.objects.filter(profile__in=team.profiles.all()).order_by('-date')[:5],
		'historic' : team.getHistoric(),
		'uri' : Solution.objects.filter(problem__judge='uri', profile__in=team.profiles.all()).order_by("problem__code").distinct("problem__code"),
		'uva' : Solution.objects.filter(problem__judge='uva', profile__in=team.profiles.all()).order_by("problem__code").distinct("problem__code"),
		'spoj' : Solution.objects.filter(problem__judge='spoj', profile__in=team.profiles.all()).order_by("problem__code").distinct("problem__code"),
	}

	return render(request, 'teams/team.html', context)
