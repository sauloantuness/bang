from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^historic/(?P<period>\w+)/(?P<type>\w+)/(?P<id>\w+)/$', views.historic, name='historic'),
]
