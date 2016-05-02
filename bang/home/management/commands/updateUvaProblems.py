from django.core.management.base import BaseCommand
from home.models import Profile, Problem, Solution
from .uva import Uva

class Command(BaseCommand):
	def handle(self, *args, **options):
		u = Uva()
		for p in u.getProblems():
			try:
				problem = Problem.objects.get(code=p['id'], judge='uva')
			except Problem.DoesNotExist:
				problem = Problem()

			problem.code = p['id']
			problem.number = p['number']
			problem.name = p['name']
			problem.category = p['category']
			problem.solved = p['solved']
			problem.level = 0
			problem.judge = 'uva'
			problem.save()