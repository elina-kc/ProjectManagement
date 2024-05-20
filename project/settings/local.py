# Development-specific settings

from .base import INSTALLED_APPS

DEBUG = True
INSTALLED_APPS_DEV = [
    # Add development-specific apps here
    "app.task_app",
    "app.projectflow_app",
    "app.resource_app",
    "app.timetrack_app",
    "app.report_app",
    "app.auth_mgmt",
]

INSTALLED_APPS += INSTALLED_APPS_DEV

# Celery configuration for development   #update this to cloudamqp
CELERY_BROKER_URL = "amqp://guest:guest@localhost:5672/myvhost"
CELERY_RESULT_BACKEND = "amqp://guest:guest@localhost:5672/myvhost"
# CELERY_RESULT_BACKEND = "rabbitmq://localhost:5672/myvhost"
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
