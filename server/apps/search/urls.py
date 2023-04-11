from rest_framework import routers

from . import views

router = routers.SimpleRouter()

urlpatterns = []

router.register(
    r"teams", views.TeamSearchViewSet, basename="search-team"
)  # 队伍搜索

router.register(
    r"activities", views.ActivitySearchViewSet, basename="search-activity"
)  # 赛事搜索

urlpatterns += router.urls
