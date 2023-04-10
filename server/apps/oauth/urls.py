from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    OpenIdLoginView,
    UnionIdLoginView,
    WechatLoginView,
    ZqAuthLoginView,
)

router = routers.SimpleRouter()

urlpatterns = [
    path(
        "login/wechat/", WechatLoginView.as_view(), name="wechat_login"
    ),  # 微信登录
    path(
        "login/wechat/openid/", OpenIdLoginView.as_view(), name="openid_pair"
    ),  # openid登录
    path(
        "login/zq/unionid/",
        UnionIdLoginView.as_view(),
        name="zq_auth_union_id",
    ),  # ZqAuth登录
    path(
        "login/zq/",
        ZqAuthLoginView.as_view(),
        name="zq_auth_login",
    ),  # ZqAuth登录
    path(
        "login/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # 刷新token
]

urlpatterns += router.urls
