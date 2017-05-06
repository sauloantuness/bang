from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from home.models import *


@login_required
def groups(request):
	context = {
		'groups': Group.objects.all()
	}

	return render(request, 'groups/index.html', context=context)