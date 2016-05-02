from django.core.management.base import BaseCommand
from home.models import Profile, Problem, Solution
from .uva import Uva
from datetime import datetime

class Command(BaseCommand):
	def handle(self, *args, **options):
		for profile in Profile.objects.all():
			print(profile.name)
			if not profile.uvaId:
				print('No UVa user.\n')
				continue
			u = Uva(profile.uvaId)
			solutions = u.getSolutions().items()
			print("%d solutions." % len(solutions))

			for code, time in solutions:
				problem = Problem.objects.get(code=code, judge='uva')
				try:
					solution = Solution.objects.get(problem=problem, profile=profile)
				except Solution.DoesNotExist:
					solution = Solution()

				solution.date = datetime.fromtimestamp(time)
				solution.problem = problem
				solution.profile = profile
				solution.save()
			print()