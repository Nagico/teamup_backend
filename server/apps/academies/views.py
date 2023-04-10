from academies.models import Academy
from academies.serializers import AcademyDetailSerializer
from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_extensions.cache.mixins import CacheResponseMixin


class AcademyViewSet(
    CacheResponseMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    """
    院系信息
    """

    queryset = Academy.objects.all()
    serializer_class = AcademyDetailSerializer
    permission_classes = [AllowAny]  # 允许任何人访问
    pagination_class = None  # 禁用分页

    @cache_response(key_func="list_cache_key_func", timeout=60 * 60 * 1)
    def list(self, request, *args, **kwargs):
        """
        重写列表获取，返回嵌套数据
        """
        result = []

        # 遍历获取所有学院
        for item in self.queryset.filter(parent=None):
            node = {
                "id": item.id,
                "name": item.name,
                "children": [],
            }

            for child in self.queryset.filter(parent=item.id):
                node["children"].append(
                    {
                        "id": child.id,
                        "name": child.name,
                    }
                )

            result.append(node)

        return Response(result)
