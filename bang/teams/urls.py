from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', 						   views.teams, name='teams'),
    url(r'^new/$', 					   views.new, name='team'),
    url(r'^update/(?P<team_id>\w+)/$', views.update, name='team'),
    url(r'^leave/(?P<team_id>\w+)/$',  views.leave, name='teams'),
    url(r'^(?P<team_id>\w+)/$', 	   views.team, name='team'),
    url(r'^skills$', views.skills, name='team'),
    url(r'^invite/(?P<answer>[a-z]+)/(?P<invite_id>[0-9]+)/$',views.teamsInvite, name='teams'),
]
