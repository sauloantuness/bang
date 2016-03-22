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
from home import views

urlpatterns = [
	url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),
	url(r'^login/$', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^settings/', include('settings.urls')),
    url(r'^problems/', include('problems.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^ranking/', include('ranking.urls')),
    url(r'', include('home.urls')),
]