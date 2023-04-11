from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Activity
from .serializers import ActivityInfoSerializer, ActivitySerializer


class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Activity.objects.order_by("-create_time")
    serializer_class = ActivitySerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "list":
            return ActivityInfoSerializer
        return ActivitySerializer
