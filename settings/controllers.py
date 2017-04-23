from home.models import *

def checkUsersAreRepeated(request, alert):
	pids = request.POST.getlist('profile-id')

	if pids[0] == pids[1] and pids[0] and pids[1]:
		request.session[alert] = True
		return True

def checkTeamName(request, alert="teamNameAlreadyExists"):
	if Team.objects.filter(name=request.POST['name']).all() or not request.POST['name']:
		request.session[alert] = True
		return True

def teamCreate(request):
	if checkUsersAreRepeated(request, alert='usersRepeatedOnCreate'):
		return

	if checkTeamName(request):
		return

	t = Team.objects.create(name=request.POST['name'])
	t.profiles.add(request.user.profile)

	for pid in request.POST.getlist('profile-id'):
		if pid:
			p = Profile.objects.get(id=pid)
			Invite.objects.create(team=t, profile=p)

	request.session['theTeamWasCreated'] = True

def teamUpdate(request):
	if checkUsersAreRepeated(request, alert='usersRepeatedOnUpdate'):
		return

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
	t = Team.objects.get(id=request.POST['id'])
	t.profiles.remove(request.user.profile)

	if t.profiles.count() == 0:
		t.delete()

	request.session['userLeftTheTeam'] = True

def getTeams(request):
	teams = []

	for t in request.user.profile.teams.all():
		members = []
		
		for profile in t.profiles.all():
			if profile == request.user.profile:
				continue

			members.append({'profile' : profile,
							 'invite' : False})
		
		for invite in t.invites.all():
			members.append({'profile' : invite.profile,
							 'invite' : True})

		team = {
			'id' : t.id,
			'name' : t.name,
			'members' : members,
		}

		teams.append(team)

	return teams

def judgesUpdate(request):
	p = Profile.objects.get(user=request.user)
	p.uriId = request.POST['uriId']
	p.uvaId = request.POST['uvaId']
	p.spojId = request.POST['spojId']
	p.save()

	request.session['judgesInformationsUpdated'] = True