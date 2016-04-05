import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pprint
class Uri():
	def __init__(self, id=None):
		self.id = id
		self.baseUrl = "https://www.urionlinejudge.com.br"
		self.userUrl  = self.baseUrl + "/judge/en/profile/%s?sort=updatetime&direction=desc&page=" % id
		self.judgeUrl = self.baseUrl + "/judge/en/problems/all?page=" 

	# From a tr tag, get the content of the problem 
	def decodeProblem(self, tr):
		tds = tr.findAll('td')
		code 	  = tds[0].getText().strip()
		name      = tds[2].getText().strip()
		category  = tds[3].getText().strip()
		solved 	  = tds[4].getText().strip()
		solved 	  = int(solved.replace(',', ''))
		level  	  = tds[5].getText().strip()

		problem = {
			'code' : code,
			'name' : name,
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
		pageNumber = 1
		problems = []
		session = requests.Session()

		while True:
			response = session.get(url + str(pageNumber))
			if response.status_code != requests.codes.ok:
				break;
			print('Page: %d' % pageNumber)	
			pageNumber += 1

			html = BeautifulSoup(response.text, 'html5lib')
			table = html.find('tbody')

			for tr in table.findAll('tr'):
				try:
					problems.append(decodeFunc(tr))

				# Last problem
				except IndexError:
					return problems

		return problems

	def getSolutions(self):
		if not self.id:
			raise NameError("User not defined.")
		else:
			return self.fetchProblems(self.userUrl, self.decodeSolution)

	def getProblems(self):
		return self.fetchProblems(self.judgeUrl, self.decodeProblem)