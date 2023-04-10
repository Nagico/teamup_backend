from rest_framework import routers

from . import views

router = routers.SimpleRouter()

urlpatterns = []

router.register(r"", views.AcademyViewSet)  # 院系信息


urlpatterns += router.urls
