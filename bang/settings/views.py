from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from home.models import Profile, Solution, Invite, Team

# Create your views here.

def teamsAdd(request):
	t = Team()
	t.name = request.POST['new-team-name']
	t.save()

	p0 = Profile.objects.get(user=request.user)
	t.profiles.add(p0)
	
	p1 = Profile.objects.get(id=request.POST['new-profile-1'])
	p2 = Profile.objects.get(id=request.POST['new-profile-2'])
	Invite(team=t, profile=p1).save()
	Invite(team=t, profile=p2).save()

def settings(request):
	if request.method == 'POST' and 'new-team' in  request.POST:
		teamsAdd(request)
		return redirect('/settings')

	if request.method == 'POST':
		p = Profile.objects.get(user=request.user)
		p.uriId = request.POST['uriId']
		p.uvaId = request.POST['uvaId']
		p.spojId = request.POST['spojId']
		p.save()

		return redirect('/settings')

	context = {
		'profile' : Profile.objects.get(user=request.user),
		'profiles' : Profile.objects.all(),
		'invites' : Invite.objects.filter(profile=request.user.profile),
		'teams' : Team.objects.filter(profiles=request.user.profile),
	}

	return render(request, 'settings/settings.html', context)