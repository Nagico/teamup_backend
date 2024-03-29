"""
Django settings for server project.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their config, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import datetime

from corsheaders.defaults import default_headers

from server.settings.util import BASE_DIR, config

SECRET_KEY = config("DJANGO_SECRET_KEY")


# region Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR.joinpath("server", "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
# endregion

# region Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
# endregion

# region Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_TZ = True
# endregion

# region Security
CORS_ORIGIN_WHITELIST = (
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "https://teamup.ziqiang.net.cn",
    "https://api.teamup.ziqiang.net.cn",
    "https://test.teamup.ziqiang.net.cn",
    "https://api.test.teamup.ziqiang.net.cn",
)

CORS_ALLOW_CREDENTIALS = True  # 允许携带cookie

# 支持前端 sentry 追踪
CORS_ALLOW_HEADERS = list(default_headers) + [
    "baggage",
    "sentry-trace",
]

# endregion

# region JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=10),
    "ALGORITHM": "HS256",
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
}
# endregion

# region 用户模型
AUTH_USER_MODEL = "users.User"
USER_ID_FIELD = "id"
# endregion

RUNSERVER_PLUS_EXCLUDE_PATTERNS = [
    "*\\Lib\\*",
    "*/Lib/*",
]

# reverse proxy scheme detect
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
