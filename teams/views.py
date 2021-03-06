from django.shortcuts import render, redirect, get_object_or_404
from home.models import Profile, Team, Invite, Solution
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import TeamForm
from functools import reduce

def teamsInvite(request, answer, invite_id):
    invite = Invite.objects.get(id=invite_id)
    profile = invite.profile
    team = invite.team
    if answer == 'yes':
        team.profiles.add(profile)

    invite.delete()

    return redirect('/settings')


@login_required
def teams(request):
    context = {
        'teams': Team.objects.all(),
    }

    return render(request, 'teams/teams.html', context)


@login_required
def team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    context = {
        'team': team,
        'solutions': {
            'uri': Solution.objects.filter(
                profile__in=team.profiles.all(),
                problem__judge='uri').distinct("problem__code").count(),
            'uva': Solution.objects.filter(
                profile__in=team.profiles.all(),
                problem__judge='uva').distinct("problem__code").count(),
            'spoj': Solution.objects.filter(
                profile__in=team.profiles.all(),
                problem__judge='spoj').distinct("problem__code").count(),
        },
        'series': team.getSkills(),
        'recentlySolved': Solution.objects.filter(
            profile__in=team.profiles.all()).order_by('-date')[:5],
        'historic': team.getHistoric(),
        'uri': Solution.objects.filter(
            problem__judge='uri',
            profile__in=team.profiles.all()
        ).order_by("problem__code").distinct("problem__code"),
        'uva': Solution.objects.filter(
            problem__judge='uva',
            profile__in=team.profiles.all()
        ).order_by("problem__code").distinct("problem__code"),
        'spoj': Solution.objects.filter(
            problem__judge='spoj',
            profile__in=team.profiles.all()
        ).order_by("problem__code").distinct("problem__code"),
    }

    return render(request, 'teams/team.html', context)


@login_required
def new(request):
    form = TeamForm(request.POST or None, request=request)
    
    context = {
        'form': form
    }

    if request.method == "POST" and form.is_valid():
        team = form.save()

        for profile in team.profiles.all():
            if profile != request.user.profile:
                Invite.objects.create(team=team, profile=profile)

        return redirect('/teams/' + str(team.pk))
    else:
        return render(request, 'teams/new.html', context)

@login_required
def update(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    form = TeamForm(request.POST or None, instance=team, request=request)

    context = {
        'form': form,
        'team': team,
        'series': team.getSkills(),
    }

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('/teams/' + str(team_id))
    else:
        return render(request, 'teams/edit.html', context)

@login_required
def leave(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    team.profiles.remove(request.user.profile)

    if team.profiles.count() == 0:
        team.delete()
        return redirect('/teams/')
    else:
        return redirect('/teams/' + str(team_id))


@login_required
def skills(request):
    skills = []
    profiles = [p for p in request.GET.getlist('profiles') if p]

    for profile in profiles:
        skills.append(Profile.objects.get(id=profile).getSkills())

    categories = ["B", "A", "S", "D", "M", "P", "G", "C", "U"]
    data = []


    for category in categories:
        data.append(
            reduce(lambda acc, s: s.problem.level + acc,
                Solution.objects.filter(
                    problem__category=category,
                    profile_id__in=profiles
                ).order_by("problem").distinct('problem'),
                0)
        )

    print(profiles)
    skills.append({
        'name': "Team",
        'data': data
    })

    return JsonResponse(skills, safe=False)


def get_score(profiles):
    problems = set()

    for profile in profiles:
        problems = problems | set(profile['problems'])

    score = reduce(lambda acc, p: p.level + acc, problems, 0)
    return score


@login_required
def best_team(request):
    profiles = []

    for profile in Profile.objects.all():
        profiles.append({
            'id': profile.id,
            'problems': [s.problem for s in profile.solution_set.all()]
        })

    team = []
    max_score = 0

    i = len(profiles) ** 2

    p3 = {
        'id': request.user.profile.id,
        'problems': [s.problem for s in profile.solution_set.all()]
    }

    for p1 in profiles:
        for p2 in profiles:
            if p1 != p2 != p3:
                score = get_score([p1, p2, p3])

                if score >= max_score:
                    max_score = score
                    team = [p1['id'], p2['id'], p3['id']]

                print(team, i)
                i = i - 1

    return JsonResponse(team, safe=False)
