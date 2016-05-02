from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from home.models import *

# Create your views here.

def teamCreate(request):
	t = Team(name=request.POST['name'])
	t.save()

	t.profiles.add(request.user.profile)
	
	for pid in request.POST.getlist('profile-id'):
		if pid:
			p = Profile.objects.get(id=pid)
			Invite(team=t, profile=p).save()

def teamUpdate(request):
	t = Team.objects.get(id=request.POST['id'])
	
	if t.name != request.POST['name']:
		t.name = request.POST['name']
		t.save()

	for invite in Invite.objects.filter(team=t):
		invite.delete()

	old_profiles = [p for p in t.profiles.all()]
	t.profiles.clear()
	t.profiles.add(request.user.profile)

	for pid in request.POST.getlist('profile-id'):
		if pid:
			p = Profile.objects.get(id=pid)
			if p in old_profiles:
				t.profiles.add(p)
			else:
				invite = Invite(team=t, profile=p)
				invite.save()

def teamLeave(request):
	t = Team.objects.get(name=request.POST['name'])
	t.profiles.remove(request.user.profile)

	if t.profiles.count() == 0:
		t.delete()

def judgesUpdate(request):
	p = Profile.objects.get(user=request.user)
	p.uriId = request.POST['uriId']
	p.uvaId = request.POST['uvaId']
	p.spojId = request.POST['spojId']
	p.save()

def getTeams(request):
	teams = []
	for t in request.user.profile.teams.all():
		team = {
			'id' : t.id,
			'name' : t.name,
			'invites' : t.invite_set.all().exclude(profile=request.user.profile),
			'profiles' : t.profiles.all().exclude(id=request.user.profile.id),
		}

		teams.append(team)

	return teams

@login_required
def settings(request):
	if request.method == 'POST':
		if 'team-create' in request.POST:
			teamCreate(request)
			return redirect('/settings')

		elif 'team-update' in request.POST:
			teamUpdate(request)
			return redirect('/settings')

		elif 'team-leave' in request.POST:
			teamLeave(request)
			return redirect('/settings')
		
		elif 'judges' in request.POST:
			judgesUpdate(request)
			return redirect('/settings')

	context = {
		'profile' 	: Profile.objects.get(user=request.user),
		'profiles' 	: Profile.objects.all().exclude(user=request.user),
		'invites' 	: Invite.objects.filter(profile=request.user.profile),
		'teams'		: getTeams(request),
	}

	return render(request, 'settings/settings.html', context)