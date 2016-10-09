from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.teams, name='teams'),
	url(r'^(?P<team_id>\w+)/$', views.team, name='team'),
	url(r'^invite/(?P<answer>[a-z]+)/(?P<invite_id>[0-9]+)/$', views.teamsInvite, name='teams'),
	url(r'^leave/(?P<team_id>[0-9]+)/$', views.teamsLeave, name='teams'),
	url(r'^delete/(?P<team_id>[0-9]+)/$', views.teamsDelete, name='teams'),
]