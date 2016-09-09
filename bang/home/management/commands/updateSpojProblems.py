from django.core.management.base import BaseCommand
from home.models import Profile, Problem, Solution
from .spoj import Spoj

class Command(BaseCommand):
	def handle(self, *args, **options):
		s = Spoj()
		problems = s.getProblems()

		for p in problems:
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
			problem.save()

		print('%d problems.' % len(problems))