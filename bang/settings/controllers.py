from home.models import *

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

def judgesUpdate(request):
	try:
		p = Profile.objects.get(user=request.user)
		p.uriId = request.POST['uriId']
		p.uvaId = request.POST['uvaId']
		p.spojId = request.POST['spojId']
		p.save()
	except:
		return 'fail'

	return 'success'