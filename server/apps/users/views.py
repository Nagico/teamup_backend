from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from teams.models import Team
from teams.serializers import TeamInfoSerializer
from users.models import User
from users.serializers import UserInfoSerializer, UserSerializer
from zq_django_util.exceptions import ApiException
from zq_django_util.response import ResponseType

from server.business.wechat.wxa import get_openid


class UserViewSet(
    viewsets.GenericViewSet,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.UpdateModelMixin,
    viewsets.mixins.RetrieveModelMixin,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.action != "retrieve":
            return self.queryset.filter(id=self.request.user.id)
        else:
            return super().get_queryset()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserInfoSerializer
        else:
            return super().get_serializer_class()

    def get_permissions(self):
        if self.action == "retrieve":
            return [AllowAny()]
        else:
            return super().get_permissions()

    def list(self, request, *args, **kwargs):
        """
        获取自己信息 or 用户id获取
        """
        nickname = request.query_params.get("nickname", None)
        student_id = request.query_params.get("student_id", None)
        if nickname and student_id:  # 传入 昵称和学号 进行 user id 查询
            if request.user.is_anonymous:
                raise ApiException(ResponseType.NotLogin)
            user = User.objects.filter(
                nickname=nickname, student_id=student_id
            ).first()
            if not user:
                raise ApiException(
                    ResponseType.ResourceNotFound, msg="您输入的昵称和学号有误，请检查后重试"
                )

            serializer = UserInfoSerializer(user)
        else:  # 获取本人用户信息
            user = self.get_queryset().first()
            serializer = self.get_serializer(user)

        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="favorites/teams")
    def favorite_teams(self, request, *args, **kwargs):
        """
        获取收藏的队伍
        """
        pass
        queryset = self.get_queryset().first().favorite_teams.all()
        serializer = TeamInfoSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="favorites/activities")
    def favorite_activities(self, request, *args, **kwargs):
        """
        获取收藏的比赛
        """
        from activities.serializers import ActivityInfoSerializer

        queryset = self.get_queryset().first().favorite_activities.all()
        serializer = ActivityInfoSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def teams(self, request, *args, **kwargs):
        """
        获取自己的队伍
        """
        queryset = Team.objects.filter(leader=request.user)
        serializer = TeamInfoSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @action(detail=False, methods=["post", "delete"], url_path="wechat")
    def wechat(self, request, *args, **kwargs):
        """
        绑定微信
        """
        user: User = self.get_queryset().first()

        if request.method == "POST":
            code = request.data.get("code", None)
            if not code:
                raise ApiException(ResponseType.ParamEmpty, detail="缺少code")

            openid = get_openid(code)

            # 如果已经有用户绑定了该微信，先解绑
            old_user = User.objects.filter(openid=openid).first()
            if old_user:
                old_user.openid = None
                old_user.save()

            user.openid = openid
            user.save()
            return Response(status=201)
        else:
            user.openid = None
            user.save()
            return Response(status=204)
