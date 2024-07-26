from django.contrib import admin
from management.models import *

admin.site.register(User)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Milestone)
admin.site.register(Notification)

