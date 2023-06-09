# pragma: no cover
import logging
import os

from celery import Celery
from celery.signals import setup_logging
from loguru import logger

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

app = Celery("server")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# django-celery-results db backend
app.loader.override_backends[
    "django-db"
] = "django_celery_results.backends.database:DatabaseBackend"


# loguru


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord):
        # Retrieve context where the logging call occurred, this happens to be in the 6th frame upward
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        mapper = {
            20: "INFO",
            10: "DEBUG",
            30: "WARNING",
            40: "ERROR",
            50: "CRITICAL",
        }
        logger_opt.log(mapper.get(record.levelno), record.getMessage())


handler = InterceptHandler()


@setup_logging.connect
def setup_logging(*args, **kwargs):
    logging.basicConfig(handlers=[InterceptHandler()], level="INFO")
