import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pprint
class Spoj():
	def __init__(self, username=None):
		self.username = username
		self.baseUrl = "http://br.spoj.com"
		self.userUrl  = self.baseUrl + "/users/%s/" % self.username
		self.judgeUrls = [
			self.baseUrl + "/problems/contest_noturno/sort=-5,start=", 
			self.baseUrl + "/problems/mineira/sort=-5,start=",
			self.baseUrl + "/problems/obi/sort=-5,start=",
			self.baseUrl + "/problems/regionais/sort=-5,start=",
			self.baseUrl + "/problems/seletivas/sort=-5,start=",
			self.baseUrl + "/problems/seletivas_ioi/sort=-5,start=",
			self.baseUrl + "/problems/sulamericana/sort=-5,start="
		]
		self.start = 0
		self.page = 1
		self.done = False
		self.new = 0

	# From a tr tag, get the content of the problem 
	def decodeProblem(self, tr):
		tds 	  = tr.findAll('td')
		number 	  = tds[0].getText().strip()
		name      = tds[1].getText().strip()
		code 	  = tds[2].getText().strip()
		solved 	  = tds[3].getText().strip()
		category  = 'U'
		level  	  = 1

		problem = {
			'number' : number,
			'name' : name,
			'code' : code,
			'category' : category,
			'solved' : solved,
			'level' : level
		}

		return problem
		
	# From a tr tag, get the content of the problem solved
	def decodeSolution(self, tr):
		tds = tr.findAll('td')
		code = tds[0].getText().strip()
		date = tds[6].getText().strip()
		date = datetime.strptime(date, '%m/%d/%y, %I:%M:%S %p')
		date = date - timedelta(hours=4)

		solution = {
			'code': code,
			'date': date
		}

		return solution

	# Get the problems from a html page from uri.
	def fetchProblems(self, url, decodeFunc):
		problems = []

		session = requests.Session()
		pos = url.rfind('/')
		print(url[:pos+1])

		while True:
			response = session.get(url + str(self.start))

			if response.status_code != requests.codes.ok:
				print('Erro ao acessar spoj')
				return problems

			print('Page: %d' % self.page)
			self.page  += 1
			self.start += 50

			html = BeautifulSoup(response.text, 'html5lib')
			table = html.find(class_='problems')

			for tr in table.findAll(class_='problemrow'):
				problem = decodeFunc(tr)
				if problems.count(problem):
					return problems

				problems.append(problem)
				pprint.pprint(problem)

	def getSolutions(self):
		if not self.id:
			print("User not defined.")
			return []
		else:
			return self.fetchProblems(self.userUrl, self.decodeSolution)

	def getProblems(self):
		return self.fetchProblems(self.judgeUrl, self.decodeProblem)


s = Spoj()
s.fetchProblems(s.judgeUrls[0], s.decodeProblem)