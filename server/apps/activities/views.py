from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

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

    @action(detail=True, methods=["post", "delete"])
    def favorites(self, request, *args, **kwargs):
        """
        收藏比赛
        """
        if request.method == "POST":
            request.user.favorite_activities.add(self.get_object())
            return Response(status=status.HTTP_201_CREATED)
        else:
            request.user.favorite_activities.remove(self.get_object())
            return Response(status=status.HTTP_204_NO_CONTENT)
