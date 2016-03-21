from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.users, name='users'),
	url(r'^(?P<user_id>[0-9]+)/$', views.user, name='user'),
]