import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
import pprint

class Spoj():
	def __init__(self, username=None):
		self.username = username
		self.baseUrl = "http://br.spoj.com/"
		self.userUrl = "http://br.spoj.com/users/%s/" % username
		self.contests = [
			'contest_noturno',
			'mineira',
			'obi',
			'regionais',
			'seletivas',
			'seletivas_ioi',
			'sulamericana',
		]

	def decodeProblem(self, tr):
		tds 	  = tr.findAll('td')
		number 	  = tds[0].getText().strip()
		name      = tds[1].getText().strip()
		code 	  = tds[2].getText().strip()
		solved 	  = tds[3].getText().strip()

		problem = {
			'number' : number,
			'name' : name,
			'code' : code,
			'solved' : solved,
		}

		return problem


	def decodeSolution(self, tr):
		tds = tr.findAll('td')
		code = tds[2].find('a').get('title')
		date = tds[1].getText().strip()
		date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

		solution = {
			'code': code,
			'date': date
		}

		if tds[3].getText().strip() == 'accepted':
			return solution
		else:
			return None


	def getContestPages(self):
		links = []

		for contest in self.contests:
			url = self.baseUrl + 'problems/' + contest
			response = requests.get(url)

			if response.status_code != requests.codes.ok:
				print("Fail in attempt to access spoj page.")
				continue

			html = BeautifulSoup(response.text, 'html5lib')
			table = html.find(class_='navigation')
			if table:
				num_pages = len(table.findAll('td')[1:-1])
				for i in range(num_pages):
					links.append(self.baseUrl + 'problems/' + contest + '/start=' + str(i * 50))
			else:
				links.append(url)

		return links

	def getSolutionPages(self):
		if not self.username:
			print("User not defined.")
			return []

		response = requests.get(self.userUrl)

		if response.status_code != requests.codes.ok:
			print("Fail in attempt to access spoj page.")
			return []

		html = BeautifulSoup(response.text, 'html5lib')
		links = []
		for a in html.find(id='content').find('table').findAll('a'):
			m = re.search("status/(\w+),", a.get('href'))
			if m:
				link = 'http://br.spoj.com/status/%s,%s/' % (m.group(1), self.username)
				links.append(link)
				print(link)
		
		return links


	def getProblems(self):
		problems = []

		for page in self.getContestPages():
			response = requests.get(page)

			if response.status_code != requests.codes.ok:
				print('Erro ao acessar spoj')
				continue

			html = BeautifulSoup(response.text, 'html5lib')
			table = html.find(class_='problems')

			for tr in table.findAll(class_='problemrow'):
				problem = self.decodeProblem(tr)
				problems.append(problem)
				pprint.pprint(problem)

		return problems


	def getSolutions(self):
		if not self.username:
			print("User not defined.")
			return []
		
		solutions = []

		for page in self.getSolutionPages():
			response = requests.get(page)

			if response.status_code != requests.codes.ok:
				print('Erro ao acessar spoj')
				continue

			html = BeautifulSoup(response.text, 'html5lib')
			table = html.find(class_='problems')

			for tr in table.findAll('tr')[1:]:
				solution = self.decodeSolution(tr)
				solutions.append(solution)
				pprint.pprint(solution)

		solutions = list(filter(lambda x: x, solutions))

		return solutions


if __name__ == "__main__":
	s = Spoj("sauloantuness")
	s.getSolutions()
