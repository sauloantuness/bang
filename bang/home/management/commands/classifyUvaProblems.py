from django.core.management.base import BaseCommand
from home.models import Profile, Problem, Solution
import requests
from .uva import Uva

class Command(BaseCommand):
	def handle(self, *args, **options):
		url = "http://uhunt.felix-halim.net/api/cpbook/3"
		r = requests.get(url)
		cp3 = None
		if r.status_code == 200:
			cp3 = r.json()

		categories = {
			'Getting Started: The Easy Problems': 'B',
			'Introduction': 'A', # Ad-Hoc
			'Data Structures and Libraries': 'D',
			'Problem Solving Paradigms': 'P',
			'Graph': 'G',
			'Mathematics': 'M',
			'String Processing': 'S',
			'(Computational) Geometry': 'C',
		}

		problemsClassified = 0
		for chapter in cp3:
			for subchapter in chapter['arr']:
				for subsubchapter in subchapter['arr']:
					for problem in subsubchapter[1:]:
						try:
							if subchapter['title'] == 'Getting Started: The Easy Problems':
								category = categories[subchapter['title']]
							else:
								category = categories[chapter['title']]
						except KeyError:
							continue
						number = str(abs(problem))

						try:
							p = Problem.objects.get(judge='uva', number=number)
							p.category = category
							p.save()
							problemsClassified += 1
						except Problem.DoesNotExist:
							print("Problem #%d is not in the database." % number)

		print("Problems classified: ", problemsClassified)




