from django.http import JsonResponse
from datetime import datetime, timedelta
from home.models import Solution


def historic(request, period):
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
        problems_solved.append(
            Solution.objects.filter(
                date__range=[day, day + timedelta(days=interval)]
            ).count())

    days = [d.strftime(mask) for d in days]

    return JsonResponse({
        'xAxis': days,
        'series': problems_solved
    })
