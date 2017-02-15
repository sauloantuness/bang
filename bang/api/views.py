from django.http import JsonResponse
from datetime import datetime, timedelta
from home.models import Solution, Team, Profile


def historic(request, period, type, id):
    now = datetime.now().date()

    if period == 'week':
        interval = 1
        amount = 7
        mask = '%d/%m'

    elif period == 'month':
        interval = 1
        amount = 30
        mask = '%d/%m'

    elif period == 'year':
        interval = 30
        amount = 12
        mask = '%b'
        now = now.replace(day=1)


    days = [now - timedelta(days=x * interval) for x in range(amount)]
    days.reverse()

    problems_solved = []
    for day in days:
        if type == 'group':
            problems_solved.append(Solution.objects.filter(date__range=[day, day + timedelta(days=interval)]).count())
        elif type == 'team':
            problems_solved.append(Solution.objects.filter(
                date__range=[day, day + timedelta(days=interval)],
                profile__in=Team.objects.get(pk=id).profiles.all()).count())
        elif type == 'profile':
            problems_solved.append(Solution.objects.filter(
                date__range=[day, day + timedelta(days=interval)],
                profile__id=id).count())

    days = [d.strftime(mask) for d in days]

    return JsonResponse({
        'xAxis': days,
        'series': problems_solved
    })
