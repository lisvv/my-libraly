import os

from celery import Celery, Task

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_library.settings")
app = Celery("my_library")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
