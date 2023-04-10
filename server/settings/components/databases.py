from loguru import logger

from server.settings.components.configs import DatabaseConfig

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DATABASES = DatabaseConfig.get()

logger.success(f"Database connect to: {DATABASES['default']['HOST']}")
