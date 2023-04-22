from rest_framework_extensions.routers import ExtendedSimpleRouter

from .views import ChatViewSet

router = ExtendedSimpleRouter()

urlpatterns = []

router.register(r"", ChatViewSet, basename="chat")

urlpatterns += router.urls
