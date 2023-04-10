# Celery Configuration Options
from server.settings.util import config

CELERY_TIMEZONE = "Asia/Shanghai"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_RESULT_EXTENDED = True
CELERY_BROKER_URL: str = config("CELERY_BROKER_URL", "")

assert CELERY_BROKER_URL, "CELERY_BROKER_URL is required"

CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "celery"

DJANGO_CELERY_RESULTS_TASK_ID_MAX_LENGTH = 191

CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
