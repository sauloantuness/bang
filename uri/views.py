from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


@login_required
def authorization(request):
	request.user.profile.uri_authorization = True
	request.user.profile.uriId = request.GET['user']
	request.user.profile.save()

	return redirect('/settings')