from chat.models import Message
from chat.serializers import ChatSerializer
from django.core.cache import caches
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

unread_cache = caches["unread"]


class ChatViewSet(
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Message.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [AllowAny]
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

    @action(methods=["post"], detail=True)
    def read(self, request, pk=None):
        message = self.get_object()
        message.read = True
        message.save()
        return Response(status=status.HTTP_200_OK)
