"""bang URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/',     admin.site.urls),
    url('',             include('social_django.urls', namespace='social')),
    url(r'',            include('home.urls')),
    url(r'^settings/',  include('settings.urls')),
    url(r'^problems/',  include('problems.urls')),
    url(r'^users/',     include('users.urls')),
    url(r'^ranking/',   include('ranking.urls')),
    url(r'^teams/',     include('teams.urls')),
    url(r'^contests/',  include('contests.urls')),
    url(r'^api/',       include('api.urls')),
    url(r'^groups/',    include('groups.urls')),
    url(r'^uri/',       include('uri.urls')),
    url(r'^trainning/', include('trainning.urls')),
    url(r'^aamas2017/', include('aamas.urls')),
]