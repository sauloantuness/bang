from django.shortcuts import render
from home.models import Solution, Problem

# Create your views here.

def uri():
	return Solution.objects.filter(problem__judge='uri').order_by('problem__code')

def uva():
	return Solution.objects.filter(problem__judge='uva').order_by('problem__code')

def spoj():
	return Solution.objects.filter(problem__judge='spoj').order_by('problem__code')

def problems(request):
	context = {
		'uri' : uri(),
		'uva' : uva(),
		'spoj' : spoj(),
	}

	return render(request, 'problems/problems.html', context)

def problem(request, problem_id):
	solutions = Solution.objects.filter(problem__id=problem_id)
	problem = solutions[0].problem
	context = {
		'solutions' : solutions,
		'problem' : problem,
	} 
	return render(request, 'problems/problem.html', context)