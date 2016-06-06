from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from home.models import *
from .controllers import *

# Create your views here.

@login_required
def settings(request):
	if request.method == 'POST':
		if 'team-create' in request.POST:
			teamCreate(request)

		elif 'team-update' in request.POST:
			teamUpdate(request)

		elif 'team-leave' in request.POST:
			teamLeave(request)
		
		elif 'judges' in request.POST:
			judgesUpdate(request)

	context = {
		'profile' 	: Profile.objects.get(user=request.user),
		'profiles' 	: Profile.objects.order_by('name').exclude(user=request.user),
		'invites' 	: Invite.objects.filter(profile=request.user.profile),
		'teams'		: getTeams(request),
		'alerts'	:
			{
				'userLeftTheTeam' : request.session.pop('userLeftTheTeam', False),
				'theTeamWasCreated' : request.session.pop('theTeamWasCreated', False),
				'usersRepeatedOnCreate' : request.session.pop('usersRepeatedOnCreate', False),
				'usersRepeatedOnUpdate' : request.session.pop('usersRepeatedOnUpdate', False),
				'teamNameAlreadyExists' : request.session.pop('teamNameAlreadyExists', False),
				'judgesInformationsUpdated' : request.session.pop('judgesInformationsUpdated', False),
			}
	}

	return render(request, 'settings/settings.html', context)