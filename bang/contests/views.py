from django.shortcuts import render, redirect
from home.models import Contest, Profile, Problem, Solution
from datetime import datetime, timedelta

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

def contestsDelete(request, contest_id):
	c = Contest.objects.get(id=contest_id).delete()
	return redirect('/contests/')

def contestsLeave(request, contest_id):
	c = Contest.objects.get(id=contest_id)
	p = Profile.objects.get(user=request.user)
	c.users.remove(p)
	return redirect('/contests/' + contest_id + '/')

def contestsJoin(request, contest_id):
	p = Profile.objects.get(user=request.user)
	c = Contest.objects.get(id=contest_id)
	c.users.add(p)
	c.save()

	selectProblems(contest)

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

def contestsContest(request, contest_id):
	
	context = {
		'contest' : Contest.objects.get(id=contest_id),
		'problems' : Problem.objects.filter(contest__id=contest_id),
		'scores' : []
	}
	contest = Contest.objects.get(id=contest_id)
	profiles = Profile.objects.filter(contests__id=contest_id)
	problems = Problem.objects.filter(contest__id=contest_id)
	solutions = Solution.objects.filter(problem__in=problems, profile__in=profiles)

	if request.user.profile.contests.filter(id=contest_id):
		print('esta aqui ')

	for profile in profiles:
		score = {
			'profile' : profile,
			'solutions' : [],
			'solved' : 0,
			'time' : 0
		}
		for problem in problems:
			try:
				solution = solutions.get(profile=profile, problem=problem)
				timeSolution =  solution.date - contest.date
				timeSolution = int(timeSolution.total_seconds()/60)
				maxTimeToSolution = contest.date + timedelta(minutes=contest.duration)
				maxTimeToSolution = maxTimeToSolution - contest.date
				maxTimeToSolution = int(maxTimeToSolution.total_seconds()/60)

				if timeSolution < 0:
					score['solutions'].append('B')
					score['solved'] += 1
				elif timeSolution > maxTimeToSolution:
					score['solutions'].append('A')
				else:
					score['solutions'].append(timeSolution)
					score['solved'] += 1
					score['time'] += timeSolution

			except Solution.DoesNotExist:
				score['solutions'].append("")

		context['scores'].append(score)

	context['scores'] = sorted(context['scores'], key=sortkeypicker(['-solved', 'time']))

	return render(request, 'contests/contests-contest.html', context)

def contestsNew(request):
	if request.method == 'POST':
		c = Contest()
		c.name = request.POST['name']
		c.date = datetime.strptime(request.POST['date'] + ' ' + request.POST['time'], "%Y-%m-%d %H:%M")
		c.duration = int(request.POST['duration'])
		c.owner = Profile.objects.get(user=request.user)
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

def contestsEdit(request, contest_id):
	if request.method == 'POST':
		c = Contest.objects.get(id=contest_id)
		c.name = request.POST['name']
		c.date = datetime.strptime(request.POST['date'] + ' ' + request.POST['time'], "%Y-%m-%d %H:%M")
		c.duration = int(request.POST['duration'])
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

def status(contest):
	now = datetime.now()

	if now < contest.date:
		return 'waiting'
	elif now < contest.date + timedelta(minutes=contest.duration):
		return 'running'
	else:
		return 'ended'


def contests(request):
	context = {
		'contests' : [],
	}
	
	for c in Contest.objects.all().order_by('-date'):
		contest = {
			'contest': c,
			'status' : status(c),
			'users' : c.users.count(),
			'problems' : c.problems.count(),
		}

		print(contest)
		context['contests'].append(contest)

	return render(request, 'contests/contests.html', context)