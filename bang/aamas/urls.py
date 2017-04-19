from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.bang, name='bang'),
    url(r'^gta$', views.gta, name='gta'),
]
