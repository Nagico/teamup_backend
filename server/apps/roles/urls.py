from rest_framework import routers

from . import views

router = routers.SimpleRouter()

urlpatterns = []

router.register(r"", views.RoleViewSet)  # 角色


urlpatterns += router.urls
