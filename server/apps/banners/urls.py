from rest_framework import routers

from . import views

router = routers.SimpleRouter()

urlpatterns = []

router.register(r"", views.BannerViewSet)  # 轮播图

urlpatterns += router.urls
