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
			return redirect('/settings')

		elif 'team-update' in request.POST:
			teamUpdate(request)
			return redirect('/settings')

		elif 'team-leave' in request.POST:
			teamLeave(request)
			return redirect('/settings')
		
		elif 'judges' in request.POST:
			context = {
				'judgeAlert' : judgesUpdate(request),
			}
			return redirect('/settings', judgeAlert=judgesUpdate(request))

	context = {
		'profile' 	: Profile.objects.get(user=request.user),
		'profiles' 	: Profile.objects.all().exclude(user=request.user),
		'invites' 	: Invite.objects.filter(profile=request.user.profile),
		'teams'		: getTeams(request),
	}

	return render(request, 'settings/settings.html', context)