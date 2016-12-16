from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^historic/(?P<period>\w+)/$', views.historic, name='historic'),
]
