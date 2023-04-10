from rest_framework import routers

from . import views

router = routers.SimpleRouter()

urlpatterns = []

router.register(r"", views.AsyncTaskViewSet, basename="async_task")  # 任务状态

urlpatterns += router.urls
