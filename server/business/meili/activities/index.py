from activities.models import Activity
from requests import Request
from zq_django_util.utils.meili.index import BaseIndex, BaseIndexHelper
from zq_django_util.utils.meili.response import SearchResult

from server.business.meili.activities.serializers import ActivityIndexSerializer


class ActivityIndex(BaseIndex):
    index_uid = "activities"

    searchable_attributes = [
        "title",
        "introduction",
        "information",
    ]


class ActivityIndexHelper(BaseIndexHelper):
    queryset = Activity.objects.all()
    serializer_class = ActivityIndexSerializer
    index_class = ActivityIndex

    def search_with_request(
        self, query: str, request: Request, **kwargs
    ) -> SearchResult:
        return super().search_with_request(
            query,
            request,
            **kwargs,
        )
