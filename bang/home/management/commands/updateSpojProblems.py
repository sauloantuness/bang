from django.core.management.base import BaseCommand
from home.models import Profile, Problem, Solution
from .spoj import Spoj

class Command(BaseCommand):
	def handle(self, *args, **options):
		s = Spoj()

		for p in s.getProblems():
			try:
				problem = Problem.objects.get(code=p['code'], judge='spoj')
			except Problem.DoesNotExist:
				problem = Problem()

			problem.name = p['name']
			problem.code = p['code']
			problem.number = p['number']
			problem.solved = p['solved']

			problem.category = 'U'
			problem.level = 0
			problem.judge = 'spoj'
			print(problem)
			problem.save()