from django.core.management.base import BaseCommand
from home.models import Profile, Problem, Solution
from .uri import Uri

class Command(BaseCommand):
	def handle(self, *args, **options):
		u = Uri()
		while not u.done:
			problems = u.getProblems()

			if not problems:
				break

			for p in problems:
				try:
					problem = Problem.objects.get(code=p['code'], judge='uri')
				except Problem.DoesNotExist:
					problem = Problem()

				problem.code = p['code']
				problem.name = p['name']
				problem.category = p['category'][0]
				problem.solved = p['solved']
				problem.level = p['level']
				problem.judge = 'uri'
				problem.save()