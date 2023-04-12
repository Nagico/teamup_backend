from server.settings.util import config

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [{"address": config("CACHE_URL")}],
        },
    },
}
