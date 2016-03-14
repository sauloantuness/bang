# SETUP
---
# Start the virtualenv
virtualenv -p python3 <envname>

# Activate
<envname>$ source bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Django
pip install Django

# Install python-social-auth
pip install python-social-auth

# PSA
---
Set config.py

# Installed Apps
INSTALLED_APPS = (
	'social.apps.django_app.default',
	...
)

# Migrate
python manage.py migrate

# URL PATTERNS
from django.conf.urls import url, include
urlpatterns = patterns('',
    url('', include('social.apps.django_app.urls', namespace='social'))
    ...
)

# Context Processors
TEMPLATE_CONTEXT_PROCESSORS = (
    ...
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

# DJANGO
---
# Start the project
django-admin startproject <projectname>

## Start the app
python manage.py startapp <appname>

# URL
---
# Set the url of the project
url(r'^example/', include('<appname>.urls')),

# Set the url of the app
url(r'^$', views.viewname, name=viewname)),

# VIEW
---
# Create a view
def viewName(request):
    return HttpResponse("hello")

# Run server
python manage.py runserver

# Edit settings.py
TIME_ZONE = 'America/Sao_Paulo'

# Migrate
The migrate command looks at the INSTALLED_APPS setting and creates any necessary database tables according to the database settings in your projectname/settings.py file and the database migrations shipped with the app.

python manage.py migrate

# Create Models

from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField(default=0)

# Activating Models

setings.py

INSTALLED_APPS = [
    'appname.apps.AppnameConfig',
    ...
]

python manage.py makemigrations appname

By running makemigrations, you’re telling Django that you’ve made some changes to your models (in this case, you’ve made new ones) and that you’d like the changes to be stored as a migration.

Migrations are how Django stores changes to your models (and thus your database schema) - they’re just files on disk.

Now, run migrate again to create those model tables in your database:

python manage.py migrate

# Creating an admin user

python manage.py createsuperuser

# Make the poll app modifiable in the admin

appname/admin.py

from django.contrib import admin

from .models import Question

admin.site.register(Question)