from django.shortcuts import render, redirect
from home.models import Profile, Team, Invite

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