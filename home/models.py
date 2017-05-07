from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from functools import reduce


class Institution(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=100)
    picture = models.CharField(max_length=500)
    secret_key = models.CharField(max_length=100)
    secret_key_coach = models.CharField(max_length=100, blank=True)
    secret_key_visitor = models.CharField(max_length=100, blank=True)
    institution = models.ForeignKey(Institution, related_name='groups')

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    picture = models.CharField(max_length=500)
    email = models.CharField(max_length=500, blank=True)
    facebookId = models.CharField(max_length=100)
    uriId = models.CharField(max_length=50, blank=True)
    uvaId = models.CharField(max_length=50, blank=True)
    spojId = models.CharField(max_length=50, blank=True)
    group = models.ForeignKey(Group, null=True, related_name='profiles')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def is_judges_filled(self):
        return self.uriId and self.uvaId and self.spojId

    def getUriLink(self):
        if self.uriId:
            return 'https://www.urionlinejudge.com.br/judge/en/users/profile/' + self.uriId
        return '#'

    def getUvaLink(self):
        if self.uvaId:
            return 'https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_authorstats&userid=' + self.uvaId
        return '#'

    def getSpojLink(self):
        if self.spojId:
            return 'http://br.spoj.com/users/' + self.spojId
        return '#'

    def getSkills(self):
        data = [
            reduce(lambda acc, s: s.problem.level + acc, self.solution_set.filter(problem__category="B"), 0),
            reduce(lambda acc, s: s.problem.level + acc, self.solution_set.filter(problem__category="A"), 0),
            reduce(lambda acc, s: s.problem.level + acc, self.solution_set.filter(problem__category="S"), 0),
            reduce(lambda acc, s: s.problem.level + acc, self.solution_set.filter(problem__category="D"), 0),
            reduce(lambda acc, s: s.problem.level + acc, self.solution_set.filter(problem__category="M"), 0),
            reduce(lambda acc, s: s.problem.level + acc, self.solution_set.filter(problem__category="P"), 0),
            reduce(lambda acc, s: s.problem.level + acc, self.solution_set.filter(problem__category="G"), 0),
            reduce(lambda acc, s: s.problem.level + acc, self.solution_set.filter(problem__category="C"), 0),
            reduce(lambda acc, s: s.problem.level + acc, self.solution_set.filter(problem__category="U"), 0),
        ]

        return {
            'name': self.user.first_name,
            'data': data,
            'pointPlacement': 'on',
        }


class Problem(models.Model):
    code = models.CharField(max_length=50)
    number = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    solved = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    judge_choices = (('uri', 'URI'),
                     ('uva', 'UVa'),
                     ('spoj', 'SPOJ'))
    judge = models.CharField(max_length=4, choices=judge_choices)
    category_choices = (('B', 'Beginner'),
    					('A', 'Ad-Hoc'),
    					('S', 'Strings'),
    					('D', 'Data Structures and Libraries'),
    					('M', 'Mathematics'),
    					('P', 'Paradigms'),
    					('G', 'Graph'),
    					('C', 'Computational Geometry'),
    					('U', 'Uncategorized'))
    category = models.CharField(max_length=1, choices=category_choices, default='U')

    def getJudgeLink(self):
        if self.judge == 'uri':
            return 'https://www.urionlinejudge.com.br/judge/en/problems/view/' + self.code
        if self.judge == 'uva':
            volume = int(self.number/100)
            return "https://uva.onlinejudge.org/external/{0}/{1}.pdf".format(volume, self.number)

        if self.judge == 'spoj':
            return 'http://br.spoj.com/problems/' + self.code

    def __str__(self):
        if self.judge == 'uva':
            return "[{0}] {1}: {2}".format(self.judge, self.number, self.name)

        return "[{0}] {1}: {2}".format(self.judge, self.code, self.name)


class Solution(models.Model):
    date = models.DateTimeField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

    def __str__(self):
        if self.problem.judge == 'uva':
            return "{0}: {1}".format(self.profile.name, self.problem.number)
        else:
            return "{0}: {1}".format(self.profile.name, self.problem.code)


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    profiles = models.ManyToManyField(Profile, related_name='teams')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def getHistoric(self, num_days=7):
        now = datetime.now().date()
        begin = now - timedelta(days=num_days)

        days = [begin + timedelta(days=x) for x in range(1, num_days + 1)]

        problems_solved = []
        for day in days:
            problems_solved.append(Solution.objects.filter(profile__in=self.profiles.all(), date__range=[day, day + timedelta(days=1)]).count())

        days = [ d.strftime('%d/%m') for d in days]
        
        return {
            'problems_solved' : problems_solved,
            'days' : days
        }

    def getSkills(self):
        skills = []

        for profile in self.profiles.all():
            skills.append(profile.getSkills())

        data = [
            Solution.objects.filter(problem__category="B", profile__in=self.profiles.all()).order_by("problem").distinct('problem').count(),
            Solution.objects.filter(problem__category="A", profile__in=self.profiles.all()).order_by("problem").distinct('problem').count(),
            Solution.objects.filter(problem__category="S", profile__in=self.profiles.all()).order_by("problem").distinct('problem').count(),
            Solution.objects.filter(problem__category="D", profile__in=self.profiles.all()).order_by("problem").distinct('problem').count(),
            Solution.objects.filter(problem__category="M", profile__in=self.profiles.all()).order_by("problem").distinct('problem').count(),
            Solution.objects.filter(problem__category="P", profile__in=self.profiles.all()).order_by("problem").distinct('problem').count(),
            Solution.objects.filter(problem__category="G", profile__in=self.profiles.all()).order_by("problem").distinct('problem').count(),
            Solution.objects.filter(problem__category="C", profile__in=self.profiles.all()).order_by("problem").distinct('problem').count(),
            Solution.objects.filter(problem__category="U", profile__in=self.profiles.all()).order_by("problem").distinct('problem').count(),
        ]

        skills.append({
                'name': "Team",
                'data': data
            })

        return skills


class Invite(models.Model):
    team = models.ForeignKey(Team, related_name='invites')
    profile = models.ForeignKey(Profile)

    def __str__(self):
        return self.team.name + ' - ' + self.profile.name


class Contest(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    duration = models.IntegerField()
    owner = models.ForeignKey(Profile)
    problems = models.ManyToManyField(Problem)
    profiles = models.ManyToManyField(Profile, related_name='contests')
    teams = models.ManyToManyField(Team, related_name='contests')
    team = models.BooleanField(default=False)
    judge_choices = (('all', 'All'),
                     ('uri', 'URI'),
                     ('uva', 'UVa'),
                     ('spoj', 'SPOJ'))
    judge = models.CharField(max_length=4, choices=judge_choices, default='all')

    B = models.IntegerField(default=0) # Beginner
    A = models.IntegerField(default=0) # Ad-Hoc
    S = models.IntegerField(default=0) # Strings
    D = models.IntegerField(default=0) # Data Structures and Libraries
    M = models.IntegerField(default=0) # Mathematics
    P = models.IntegerField(default=0) # Paradigms
    G = models.IntegerField(default=0) # Graph
    C = models.IntegerField(default=0) # Computational Geometry
    R = models.IntegerField(default=0) # Random
    # winner = models.ForeignKey(Profile)

    def getStatus(self):
        now = datetime.now()

        if now < self.date:
            return 'waiting'
        elif now < self.date + timedelta(minutes=self.duration):
            return 'running'
        else:
            return 'ended'

    def setProblems(self):
        self.problems.clear()
        profiles = self.profiles.all()
        solutions = Solution.objects.filter(profile__in=profiles)
        problems = Problem.objects.exclude(solution__in=solutions)
        if self.judge != 'all':
            problems = problems.filter(judge=self.judge)

        categories = ['B', 'A', 'S', 'D', 'M', 'P', 'G', 'C']
        for category in categories:
            amount = self.__dict__[category]
            for problem in problems.filter(category=category).order_by('-solved')[:amount]:
                self.problems.add(problem)

    def __str__(self):
        return self.name
