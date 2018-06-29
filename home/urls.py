from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', 			views.home, 	name='home'),
	url(r'^login/$', 	views.login, 	name='login'),
    url(r'^logout/$', 	views.logout, 	name='logout'),
    url(r'^about/$', 	views.about, 	name='about'),
    url(r'^privacy/$', 	views.privacy, 	name='privacy'),
]