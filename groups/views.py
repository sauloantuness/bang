from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from home.models import *


@login_required
def groups(request):
    filter = request.GET.get('filter')
    groups = []

    if filter:
        groups = [m.group for m in request.user.profile.membership_set.all()]
    else:
        groups: Group.objects.all()

    context = {
        'groups': groups,
        'filter': filter,
    }

    return render(request, 'groups/index.html', context=context)


@login_required
def new(request):
    context = {
        'groups': Group.objects.all()
    }

    return render(request, 'groups/index.html', context=context)
