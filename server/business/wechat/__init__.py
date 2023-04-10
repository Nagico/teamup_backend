from django.conf import settings
from django.core.cache import caches
from wechatpy.client import WeChatClient
from wechatpy.session import SessionStorage


class WechatCache(SessionStorage):
    def __init__(self, cache):
        self.cache = cache

    def get(self, key, default=None):
        return self.cache.get(key, default)

    def set(self, key, value, ttl=None):
        self.cache.set(key, value, timeout=ttl)

    def delete(self, key):
        self.cache.delete(key)


if settings._ENV == "test":
    from unittest import mock

    wechat_client = mock.MagicMock()
else:
    wechat_client = WeChatClient(
        settings.WECHAT_APPID,
        settings.WECHAT_SECRET,
        session=WechatCache(caches["third_session"]),
    )


ENV_VERSION = "release"
if (
    hasattr(settings, "SERVER_URL")
    and hasattr(settings, "PRODUCTION_SERVER_LIST")
    and hasattr(settings, "DEVELOPMENT_SERVER_LIST")
):
    if settings.SERVER_URL in settings.PRODUCTION_SERVER_LIST:
        ENV_VERSION = "release"
    elif settings.SERVER_URL in settings.DEVELOPMENT_SERVER_LIST:
        ENV_VERSION = "trial"
