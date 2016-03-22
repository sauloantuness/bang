from django.core.management.base import BaseCommand
from home.models import Profile, Problem, Solution
from .uri import Uri

class Command(BaseCommand):
	def handle(self, *args, **options):
		for profile in Profile.objects.all():
			print(profile.name)
			u = Uri(profile.uriId)

			for s in u.getSolutions():
				problem = Problem.objects.get(code=s['code'], judge='uri')
				try:
					solution = Solution.objects.get(problem=problem, profile=profile)
				except Solution.DoesNotExist:
					solution = Solution()

				solution.date = s['date']
				solution.problem = problem
				solution.profile = profile
				solution.save()
			print()