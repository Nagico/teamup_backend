from rest_framework_extensions.routers import ExtendedSimpleRouter

# from .views import MessageViewSet

router = ExtendedSimpleRouter()

urlpatterns = []

# router.register(r"", MessageViewSet, basename="message")

urlpatterns += router.urls
