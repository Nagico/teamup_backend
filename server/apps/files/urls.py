from rest_framework_extensions.routers import ExtendedDefaultRouter

from . import views

router = ExtendedDefaultRouter()

urlpatterns = []

router.register(r"", views.FileViewSet)

urlpatterns += router.urls
