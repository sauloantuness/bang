import requests
import json
from bs4 import BeautifulSoup
from user import User
from problem import Problem
from solved import Solved

class Uri():
	def __init__(self, user=None):
		self.user = user
		self.baseUrl  = "https://www.urionlinejudge.com.br"

		if user:
			self.userUrl  = self.baseUrl + "/judge/profile/%s/sort:Run.updatetime/direction:desc/page:" % user.uriId
		else:
			self.judgeUrl = self.baseUrl + "/judge/en/problems/all/page:" 

	# From a tr tag, get the content of the problem 
	def decodeJudgeProblem(self, tr):
		a = tr.findAll('a')
		problemId = a[0].getText()
		name      = a[1].getText()
		category  = a[2].getText()
		
		small = tr.findAll(class_='small')
		solved = small[0].getText().strip()
		level  = small[1].getText()
		
		return Problem(problemId, name, category, level, solved)

	# From a tr tag, get the content of the problem solved
	def decodeUserProblem(self, tr):
		userId = self.user.userId

		a = tr.findAll('a')
		problemId = a[0].getText()
		
		td = tr.findAll('td')
		date = td[-1].getText().strip()

		return Solved(userId, problemId, date)

	# Get the problems from a html page from uri.
	def fetchProblems(self, url, decodeFunc):
		pageNumber = 1

		session = requests.Session()
		problems = []

		print "Fetching problems"

		while True:
			response = session.get(url + str(pageNumber))
			
			if response.status_code != requests.codes.ok:
				break;

			print "Page number: %d" % pageNumber
			pageNumber += 1
			
			html = BeautifulSoup(response.text, 'html5lib')
			table = html.find('tbody')

			for tr in table.findAll('tr'):
				try:
					problems.append(decodeFunc(tr))

				# Last page
				except IndexError:
					break

		return problems

	def getProblems(self):
		if self.user:
			return self.fetchProblems(self.userUrl, self.decodeUserProblem)
		else:
			return self.fetchProblems(self.judgeUrl, self.decodeJudgeProblem)