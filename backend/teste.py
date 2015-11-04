import requests
import json
from bs4 import BeautifulSoup

def decodeJudgeProblem(tr):
	problem = {}

	a = tr.findAll('a')
	problem['code'] = a[0].getText()
	problem['name'] = a[1].getText()
	problem['category'] = a[2].getText()
	
	small = tr.findAll(class_='small')
	problem['solved'] = small[0].getText().strip()
	problem['level'] = small[1].getText()
	
	return problem

def decodeUserProblem(tr):
	problem = {}

	a = tr.findAll('a')
	problem['code'] = a[0].getText()
	
	td = tr.findAll('td')
	problem['date'] = td[-1].getText().strip()

	return problem

def fetchProblems(url, fileName, decodeFunc):
	pageNumber = 1

	session = requests.Session()
	problems = []
	f = open(fileName, "w")

	while True:
		response = session.get(url + str(pageNumber))
		
		if response.status_code != requests.codes.ok:
			break;

		print pageNumber
		print len(problems)
		pageNumber += 1
		
		html = BeautifulSoup(response.text, 'html5lib')
		table = html.find('tbody')

		for tr in table.findAll('tr'):
			try:
				problems.append(decodeFunc(tr))

			except IndexError:
				# Last page
				break

	json.dump(problems, f)
	f.close()

def getUserProblems(profile=1):
	url = "https://www.urionlinejudge.com.br/judge/profile/%s/sort:Run.updatetime/direction:desc/page:" % profile
	fileName = 'userProblems'
	fetchProblems(url, fileName, decodeUserProblem)

def getJudgeProblems():
	url = "https://www.urionlinejudge.com.br/judge/en/problems/all/page:"
	fileName = 'judgeProblems'
	fetchProblems(url, fileName, decodeJudgeProblem)

getUserProblems('39764')
getJudgeProblems()