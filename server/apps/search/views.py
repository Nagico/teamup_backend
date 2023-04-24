from activities.models import Activity
from activities.serializers import ActivityInfoSerializer
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from teams.models import Team
from teams.serializers import TeamInfoSerializer
from zq_django_util.exceptions import ApiException
from zq_django_util.response import ResponseType
from zq_django_util.utils.meili.pagination import MeiliPageNumberPagination

from server.business.meili.activities.index import ActivityIndexHelper
from server.business.meili.teams.index import TeamIndexHelper


class BaseSearchViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = None
    serializer_class = None
    pagination_class = MeiliPageNumberPagination
    helper = None

    permission_classes = [AllowAny]

    def search(self, request, *args, **kwargs):
        text = request.query_params.get("text", None)
        if text is None:
            raise ApiException(ResponseType.ParamEmpty)

        return self.helper.search_with_request(text, request)  # meili搜索

    def list(self, request, *args, **kwargs):
        queryset = self.search(request, *args, **kwargs)
        queryset.object_list = self.queryset.filter(
            id__in=[i["id"] for i in queryset.object_list]
        )  # 使用id检索数据库

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=["get"], detail=False)
    def rebuild(self, request, *args, **kwargs):
        self.helper.rebuild_index()
        return Response()

    @action(methods=["get"], detail=False, url_path="rebuild/(?P<pk>[0-9]+)")
    def rebuild_one(self, request, pk=None):
        self.helper.delete_index(pk)
        self.helper.upsert_index(pk)
        return Response()


class TeamSearchViewSet(BaseSearchViewSet):
    queryset = Team.objects.filter(public=True)
    serializer_class = TeamInfoSerializer

    helper = TeamIndexHelper()

    def search(self, request, *args, **kwargs):
        text = request.query_params.get("text", None)

        has_teacher = request.query_params.get("teacher", None)
        if has_teacher:
            has_teacher = has_teacher == "true"

        activity_ids = request.GET.getlist("activities[]", None)
        if activity_ids and len(activity_ids) > 0:
            activity_ids = [int(i) for i in activity_ids]
        else:
            activity_ids = None

        role_ids = request.GET.getlist("roles[]", None)
        if role_ids and len(role_ids) > 0:
            role_ids = [int(i) for i in role_ids]
        else:
            role_ids = None

        return self.helper.search_with_request(
            text,
            request,
            has_teacher=has_teacher,
            activity_ids=activity_ids,
            role_ids=role_ids,
        )


class ActivitySearchViewSet(BaseSearchViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivityInfoSerializer

    helper = ActivityIndexHelper()
