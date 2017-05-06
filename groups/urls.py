from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.groups, name='groups'),
    # url(r'^new/$', views.contestsNew, name = 'contests'),
]