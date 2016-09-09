from django.core.management.base import BaseCommand
from home.models import Profile, Problem, Solution
from .spoj import Spoj
from datetime import datetime

class Command(BaseCommand):
	def handle(self, *args, **options):
		for profile in Profile.objects.all():
			print(profile.name)
			if not profile.spojId:
				print('No SPOJ user.\n')
				continue

			s = Spoj(profile.spojId)
			solutions = s.getSolutions()
			print("%d solutions." % len(solutions))

			for s in solutions:
				try:
					problem = Problem.objects.get(code=s['code'], judge='spoj')
				except Problem.DoesNotExist:
					print('SPOJ is missing problem: ', s['code'])
					continue
				try:
					solution = Solution.objects.get(problem=problem, profile=profile)
				except Solution.DoesNotExist:
					solution = Solution()

				if not solution.date or s['date'] < solution.date:
					solution.date = s['date']
				solution.problem = problem
				solution.profile = profile
				solution.save()
			print()