from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Profile)
admin.site.register(Problem)
admin.site.register(Solution)
admin.site.register(Contest)
admin.site.register(Team)
admin.site.register(Invite)