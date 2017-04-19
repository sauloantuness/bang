from django.shortcuts import render


def bang(request):
    return render(request, 'aamas/bang.html')

def gta(request):
    return render(request, 'aamas/gta.html')
