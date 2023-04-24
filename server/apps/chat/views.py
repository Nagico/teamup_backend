from uuid import UUID

from chat.models import Message
from chat.serializers import ChatSerializer
from django.core.cache import caches
from django.db.models import Q, Subquery
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

unread_cache = caches["unread"]


class ChatViewSet(
    viewsets.mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Message.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["type"]

    def get_queryset(self):
        if self.request.user.is_authenticated:  # 已登录用户
            other = self.request.query_params.get("other")  # 对方用户id
            if other:  # 传入对方id，查询与对方的聊天记录
                return self.queryset.filter(
                    Q(sender=self.request.user, receiver=other)
                    | Q(sender=other, receiver=self.request.user)
                )
        else:  # 查询通知信息
            return self.queryset.filter(sender=None)

    def list(self, request, *args, **kwargs):
        message_id = self.request.query_params.get("before", None)
        limit = int(self.request.query_params.get("limit", 20))

        if message_id:  # 传入id，查询id之前的消息
            message = Message.objects.filter(id=UUID(message_id)).values(
                "create_time"
            )
            queryset = self.get_queryset().filter(
                create_time__lt=Subquery(message)
            )[:limit]
        else:
            queryset = self.get_queryset()[:limit]

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
