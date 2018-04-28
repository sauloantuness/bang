from django.db.models import Count
from datetime import datetime, timedelta


def email(backend, response):
    if backend.name == 'facebook':
        return response['email']

    elif backend.name == 'google-oauth2':
        return response['emails'][0]['value']


def set_profile(backend, response, user, is_new=False, *args, **kwargs):
    from home.models import Profile    
    profile = Profile.objects.filter(email=email(backend, response)).first()

    if not profile:
        profile = Profile()

    if backend.name == 'facebook':
            profile.name = response['name']
            profile.picture = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
            profile.facebookId = response['id']
            profile.email = response['email']

    elif backend.name == 'google-oauth2':
        profile.name = response['displayName']
        profile.picture = response['image']['url'].split('?')[0]
        profile.email = response['emails'][0]['value']

    profile.user = user
    profile.save()


def formatTime(minutes):
    if minutes < 60:
        return "%d min" % minutes

    if minutes % 60 == 0:
        return "%d h" % int(minutes / 60)

    return "%d h %d min" % (minutes / 60, minutes % 60)


def getContests(orderBy='-date'):
    from home.models import Contest
    '''
    Return a list of contests order by the -date.
    '''
    contests = []

    for c in Contest.objects.all().order_by(orderBy):
        contest = {
            'contest': c,
            'duration': formatTime(c.duration),
            'num_profiles': c.profiles.count(),
            'num_problems': c.problems.count(),
        }

        contests.append(contest)

    return contests

def get_solution_for_judge(judge, groups=[]):
    from home.models import Solution
    if groups:
        ids_group = [x.pk for x in groups]
        return Solution.objects.filter(profile__group__pk__in=ids_group).filter(problem__judge=judge).distinct('problem').count()      
    return  Solution.objects.filter(problem__judge=judge).distinct('problem').count()

def get_solutions_amout(groups=[]):
    '''
    Return the amount of distinct problems solved by group.
    '''
    return {
        'uri': get_solution_for_judge('uri', groups),
        'uva': get_solution_for_judge('uva', groups),
        'spoj': get_solution_for_judge('spoj', groups),
    }

def getLastSolutions():
    from home.models import Solution
    '''
    Return a list with the last solutions.
    '''
    return Solution.objects.all().order_by('-date')[:10]


def getHistoric():
    from home.models import Solution
    '''
    Return a list of problems solved by day of the user, team or group.
    '''
    now = datetime.now().date()
    begin = now - timedelta(days=7)

    days = [begin + timedelta(days=x) for x in range(1, 8)]

    problems_solved = []
    for day in days:
        problems_solved.append(Solution.objects.filter(date__range=[day, day + timedelta(days=1)]).count())

    days = [d.strftime('%d/%m') for d in days]

    return {
        'problems_solved': problems_solved,
        'days': days,
    }


def getTrends():
    from home.models import Profile
    '''
    Return a list of profiles with more solutions in the last 7 days.
    '''
    d = datetime.now().date() - timedelta(days=7)

    return {
        'profiles': Profile.objects.filter(solution__date__gt=d).annotate(num_solutions=Count('solution')).order_by('-num_solutions')[:5]
    }


def group_check(user):
    return user.profile.group