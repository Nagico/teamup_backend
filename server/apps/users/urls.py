from rest_framework_extensions.routers import ExtendedSimpleRouter
from users.views import UserViewSet

router = ExtendedSimpleRouter()

urlpatterns = []

router.register(r"", UserViewSet, basename="user")

urlpatterns += router.urls
