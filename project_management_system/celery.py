from __future__ import absolute_import, unicode_literals
# import os
# from celery import Celery

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_management_system.settings')

# app = Celery('project_management_system')
# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()
# celery.py
import os
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_management_system.settings')

app = Celery('project_management_system')

app.conf.enable_utc=False
app.conf.update(timezone='Asia/Kolkata')

app.config_from_object(settings, namespace='CELERY')


app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
