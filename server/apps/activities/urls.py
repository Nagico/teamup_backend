from rest_framework_extensions.routers import ExtendedSimpleRouter

from .views import ActivityViewSet

router = ExtendedSimpleRouter()

urlpatterns = []

router.register(r"", ActivityViewSet, basename="activity")

urlpatterns += router.urls
