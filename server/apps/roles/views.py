from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from roles.models import Role
from roles.serializers import RoleSerializer


class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [AllowAny]
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = {"parent": ["exact", "isnull"]}

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
