from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework import routers
from zq_django_util.utils.views import APIRootViewSet

router = routers.SimpleRouter()

router.register("", APIRootViewSet, basename="test")

urlpatterns = [
    path("admin/", admin.site.urls),  # admin 后台管理
    path("api-auth/", include("rest_framework.urls")),  # drf 自带的登录认证
    path(
        "favicon.ico",
        RedirectView.as_view(
            url="https://zq-public-oss.oss-cn-hangzhou.aliyuncs.com/zq-auth/backend/static/static/favorite.ico"
        ),
    ),
    path("auth/", include("oauth.urls")),  # 登录
    path("users/", include("users.urls")),  # 用户
    path("academies/", include("academies.urls")),  # 学院
    path("roles/", include("roles.urls")),  # 角色
    path("teams/", include("teams.urls")),  # 队伍
]

urlpatterns += router.urls

handler404 = "zq_django_util.exceptions.views.bad_request"
handler500 = "zq_django_util.exceptions.views.server_error"

if settings.DEBUG:  # pragma: no cover
    import debug_toolbar  # noqa: WPS433
    from django.conf.urls.static import static  # noqa: WPS433

    urlpatterns = [
        # URLs specific only to django-debug-toolbar:
        path("__debug__/", include(debug_toolbar.urls)),
        *urlpatterns,
        # Docs:
        path("docs/schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            "docs/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),  # swagger接口文档
        path(
            "docs/redoc/",
            SpectacularRedocView.as_view(url_name="schema"),
            name="redoc",
        ),  # redoc接口文档
        # Serving media files in development only:
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
        *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    ]
