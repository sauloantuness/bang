from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from home.models import *
from home.utils import *

# Create your views here.

def selectProblems(contest):
	contest.problems.clear()
	categories = ['A', 'B', 'S', 'D', 'M', 'G', 'P', 'C']
	users = contest.users.all()
	solutions = Solution.objects.filter(profile__in=users)
	problems = Problem.objects.exclude(solution__in=solutions)

	for category in categories:
		amount = contest.__dict__[category]
		for problem in problems.filter(category=category).order_by('-solved')[:amount]:
			contest.problems.add(problem)
			print(problem)

@login_required
def contestsDelete(request, contest_id):
	Contest.objects.get(id=contest_id).delete()
	return redirect('/contests/')

@login_required
def contestsLeave(request, contest_id):
	c = Contest.objects.get(id=contest_id)
	c.profiles.remove(request.user.profile)
	c.setProblems()

	return redirect('/contests/' + contest_id + '/')

@login_required
def contestsJoin(request, contest_id):
	c = Contest.objects.get(id=contest_id)
	c.profiles.add(request.user.profile)
	c.save()

	c.setProblems()

	return redirect('/contests/' + contest_id + '/')

def sortkeypicker(keynames):
	from operator import itemgetter as i
	from functools import cmp_to_key

	negate = set()
	for i, k in enumerate(keynames):
		if k[:1] == '-':
			keynames[i] = k[1:]
			negate.add(k[1:])
	def getit(adict):
		composite = [adict[k] for k in keynames]
		for i, (k, v) in enumerate(zip(keynames, composite)):
			if k in negate:
				composite[i] = -v
		return composite
	return getit

def evaluateSolution(contest, solution):
	timeSolution = solution.date - contest.date
	timeSolution = int(timeSolution.total_seconds()/60)
	maxTimeToSolution = contest.date + timedelta(minutes=contest.duration)
	maxTimeToSolution = maxTimeToSolution - contest.date
	maxTimeToSolution = int(maxTimeToSolution.total_seconds()/60)

	if timeSolution < 0:
		return 'B'
	elif timeSolution > maxTimeToSolution:
		return 'A'
	else:
		return timeSolution
	
def getSolutionsOfContest(profile, contest):
	solutions = []
	for problem in contest.problems.all():
		try:
			solution = Solution.objects.get(profile=profile, problem=problem)
			solutions.append(evaluateSolution(contest, solution))

		except Solution.DoesNotExist:
			solutions.append("")

	return solutions

def getBestSolutions(solutions, profileSolutions):
	for i in range(0, len(solutions)):
		if solutions[i] == "":
			solutions[i] = profileSolutions[i]
		
		elif profileSolutions[i] == "":
			pass

		elif solutions[i] == "B":
			pass
		
		elif profileSolutions[i] == "B":
			solutions[i] = profileSolutions[i]

		elif type(profileSolutions[i]) is int:
			if type(solutions[i]) is int:
				solutions[i] = min(solutions[i], profileSolutions[i])
			else:
				solutions[i] = profileSolutions[i]

	return solutions


def getSolutionsOfContestByTeam(team, contest):
	num_problems = contest.problems.count()
	solutions = [""] * num_problems

	for profile in team.profiles.all():
		profileSolutions = getSolutionsOfContest(profile, contest)
		solutions = getBestSolutions(solutions, profileSolutions)

	return solutions

def countScore(score):
	for solution in score['solutions']:
		if type(solution) is int:
			score['solved'] += 1
			score['time'] += solution

	return score

def getContestScore(contest):
	scores = []

	if contest.team:
		for team in contest.teams.all():
			score = {
				'team' : team,
				'solutions' : getSolutionsOfContestByTeam(team, contest),
				'solved' : 0,
				'time' : 0
			}

			scores.append(countScore(score))

	else:
		for profile in contest.profiles.all():
			score = {
				'profile' : profile,
				'solutions' : getSolutionsOfContest(profile, contest),
				'solved' : 0,
				'time' : 0
			}

			scores.append(countScore(score))

	scores = sorted(scores, key=sortkeypicker(['-solved', 'time']))
	return scores

@login_required
def contestsContest(request, contest_id):
	contest = Contest.objects.get(id=contest_id)
	context = {
		'contest': contest,
		'duration': formatTime(contest.duration),
		'problems': contest.problems.all(),
		'scores': getContestScore(contest),
		'now': datetime.now().timestamp() * 1000,
	}

	return render(request, 'contests/contests-contest.html', context)

@login_required
def contestsNew(request):
	if request.method == 'POST':
		c = Contest()
		c.name = request.POST['name']
		c.date = datetime.strptime(request.POST['date'] + ' ' + request.POST['time'], "%m/%d/%Y %H:%M")
		c.duration = int(request.POST['duration'])
		c.owner = request.user.profile
		c.team = bool(int(request.POST['team']))
		c.judge = request.POST['judge']
		c.B = int(request.POST['B'])
		c.A = int(request.POST['A'])
		c.S = int(request.POST['S'])
		c.D = int(request.POST['D'])
		c.M = int(request.POST['M'])
		c.P = int(request.POST['P'])
		c.G = int(request.POST['G'])
		c.C = int(request.POST['C'])

		c.save()

		return redirect('/contests/')
	else:
		return render(request, 'contests/contests-new.html')

@login_required
def contestsEdit(request, contest_id):
	if request.method == 'POST':
		c = Contest.objects.get(id=contest_id)
		c.name = request.POST['name']
		c.date = datetime.strptime(request.POST['date'] + ' ' + request.POST['time'], "%m/%d/%Y %H:%M")
		c.duration = int(request.POST['duration'])
		c.team = bool(int(request.POST['team']))
		c.judge = request.POST['judge']
		c.B = int(request.POST['B'])
		c.A = int(request.POST['A'])
		c.S = int(request.POST['S'])
		c.D = int(request.POST['D'])
		c.M = int(request.POST['M'])
		c.P = int(request.POST['P'])
		c.G = int(request.POST['G'])
		c.C = int(request.POST['C'])

		c.save()

		return redirect('/contests/' + contest_id + '/')

	else:
		context = {
			'contest' : Contest.objects.get(id=contest_id),
		}

		return render(request, 'contests/contests-edit.html', context)

@login_required
def contests(request):
	context = {
		'contests' : getContests(),
	}

	return render(request, 'contests/contests.html', context)