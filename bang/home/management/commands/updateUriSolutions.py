from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from home.models import Profile, Problem, Solution
from .uri import Uri

class Command(BaseCommand):
	def handle(self, *args, **options):
		def createSolution(profile, problem, date):
			solution = Solution()
			solution.profile = profile
			solution.problem = problem
			solution.date = date
			solution.save()

		for profile in Profile.objects.all():
			print(profile.name)
			uri = Uri(profile.uriId)

			while not uri.done:
				solutions = uri.getSolutions()

				if not solutions:
					break

				for s in solutions:
					try:
						problem = Problem.objects.get(code=s['code'], judge='uri')
					except Problem.DoesNotExist:
						print('URI is missing problem: ', s['code'])
						continue
					try:
						solution = Solution.objects.get(problem=problem, profile=profile)
						uri.done = True
					except Solution.DoesNotExist:
						createSolution(profile, problem, s['date'])
						uri.new += 1
						
					if uri.done:
						break
					
			print("New Solutions: ", uri.new, "\n")