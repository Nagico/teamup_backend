from banners.models import Banner
from banners.serializers import BannerDetailSerializer, BannerInfoSerializer
from rest_framework import viewsets

from server.utils.permissions import IsSuperUser, ReadOnly


class BannerViewSet(viewsets.ModelViewSet):
    """
    轮播图视图集
    """

    queryset = Banner.objects.order_by("-score")
    serializer_class = BannerInfoSerializer
    pagination_class = None
    permission_classes = [ReadOnly | IsSuperUser]

    def get_serializer_class(self):
        if self.action == "list":
            return BannerInfoSerializer
        return BannerDetailSerializer
