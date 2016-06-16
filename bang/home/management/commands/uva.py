import requests
import json
from datetime import datetime, timedelta
import pprint

class Uva():
	def __init__(self, uid=None):
		self.problemsUrl = 'http://uhunt.felix-halim.net/api/p'
		self.problemsCpUrl = 'http://uhunt.felix-halim.net/api/cpbook/3'
		self.solutionsUrl = 'http://uhunt.felix-halim.net/api/subs-user/' #/api/subs-user/{user-id}/{min-sid}.
		self.uname2uidUrl = 'http://uhunt.felix-halim.net/api/uname2uid/'
		self.uid = uid
	
	def getSolutions(self):
		r = requests.get(self.solutionsUrl + self.uid)
		if r.status_code == requests.codes.ok:
			subs = [sub for sub in r.json()['subs'] if sub[2] == 90]
			solutions = {}
			for sub in subs:
				if solutions.get(sub[1], False):
					if solutions[sub[1]] > sub[4]:
						solutions[sub[1]] = sub[4]
				else:
					solutions[sub[1]] = sub[4]

			return solutions

	def getProblems(self):
		r = requests.get(self.problemsUrl)
		if r.status_code == requests.codes.ok:
			problems = []
			for p in r.json():
				problem = {
					'id' : p[0],
					'number' : p[1],
					'name' : p[2],
					'solved' : p[3],
					'category' : 'U',
				}
				problems.append(problem)

		return problems