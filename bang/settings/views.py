from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from home.models import Profile, Solution

# Create your views here.

def settings(request):
	if request.method == 'POST':
		p = Profile.objects.get(user=request.user)
		p.uriId = request.POST['uriId']
		p.uvaId = request.POST['uvaId']
		p.spojId = request.POST['spojId']
		p.save()

		return redirect('/settings')

	else:
		context = {
			'profile' : Profile.objects.get(user=request.user)
		}

		return render(request, 'settings/settings.html', context)