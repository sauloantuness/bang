from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def set_profile(backend, response, user, is_new=False, *args, **kwargs):
    if backend.name == 'facebook':
        try:
            p = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            p = Profile()
            p.user = user
        
        p.name = response['name']
        p.picture = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
        p.facebookId = response['id']
        p.save()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    facebookId = models.CharField(max_length=100)
    picture = models.CharField(max_length=500)
    uriId = models.CharField(max_length=50, blank=True)
    uvaId = models.CharField(max_length=50, blank=True)
    spojId = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.user.username

class Problem(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    solved = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    judge_choices = (('uri', 'URI'), ('uva', 'UVA'), ('spoj', 'SPOJ'))
    judge = models.CharField(max_length=4, choices=judge_choices, default='uri')
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

    def __str__(self):
        return "[{0}] {1}: {2}".format(self.judge, self.code, self.name)

class Solution(models.Model):
    date = models.DateField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

    def __str__(self):
        return "{0}: {1}".format(self.profile.user.username, self.problem.code)