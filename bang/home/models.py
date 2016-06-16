from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    picture = models.CharField(max_length=500)
    facebookId = models.CharField(max_length=100)
    uriId = models.CharField(max_length=50, blank=True)
    uvaId = models.CharField(max_length=50, blank=True)
    spojId = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.user.username

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
            return '#'

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
    name = models.CharField(max_length=100)
    profiles = models.ManyToManyField(Profile, related_name='teams')

    def __str__(self):
        return self.name

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
