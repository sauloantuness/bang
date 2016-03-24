from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.contests, name='contests'),
	url(r'^new/$', views.contestsNew, name='contests'),
	url(r'^edit/(?P<contest_id>\w+)/$', views.contestsEdit, name='contests'),
	url(r'^join/(?P<contest_id>\w+)/$', views.contestsJoin, name='contests'),
	url(r'^leave/(?P<contest_id>\w+)/$', views.contestsLeave, name='contests'),
	url(r'^(?P<contest_id>\w+)/$', views.contestsContest, name='contests'),
]