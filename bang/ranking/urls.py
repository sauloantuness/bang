from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.ranking, name='ranking'),
	url(r'^(?P<order>\w+)/$', views.ranking, name='ranking'),
]