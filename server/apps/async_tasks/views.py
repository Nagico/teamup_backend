from async_tasks.utils import get_task_status
from celery.result import AsyncResult
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class AsyncTaskViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    def retrieve(self, request, *args, **kwargs):
        task_id = kwargs.get("pk")
        task = AsyncResult(task_id)
        response = get_task_status(task)
        return Response(response)
