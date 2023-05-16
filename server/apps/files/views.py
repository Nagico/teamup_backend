from files.models import File
from files.serializers import FileSerializer
from files.tasks import update_preview_pages
from files.utils import gen_token, handle_callback
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from users.models import User
from zq_django_util.exceptions import ApiException
from zq_django_util.response import ResponseType
from zq_django_util.utils.oss.utils import check_callback_signature


class FileViewSet(ModelViewSet):
    """
    文件视图集
    """

    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 获取当前用户的文件
        if self.action == "callback":
            return self.queryset
        return self.queryset.filter(user=self.request.user)

    def get_permissions(self):
        if self.action == "callback":
            return [AllowAny()]
        return super(FileViewSet, self).get_permissions()

    def perform_create(self, serializer):
        """
        测试

        自动更新预览页
        """
        super().perform_create(serializer)
        update_preview_pages(serializer.instance.id)

    @action(methods=["post"], detail=False)
    def token(self, request):
        """
        获取OSS直传token
        """
        user: User = request.user
        if not user.is_authenticated:
            raise ApiException(ResponseType.NotLogin, "您尚未登录，请登录后重试")

        filename = request.data.get("name")
        if not filename:
            raise ApiException(
                ResponseType.ParamValidationFailed, "请传入name参数", record=True
            )

        res = gen_token(filename, request, user)

        if res:
            return Response(res)
        else:
            raise ApiException(
                ResponseType.PermissionDenied, "您没有权限上传此文件", record=True
            )

    @action(methods=["post"], detail=True)
    def callback(self, request, pk=None):
        """
        OSS回调
        """
        if not check_callback_signature(request):
            raise ApiException(
                ResponseType.PermissionDenied, "OSS回调签名检验失败", record=True
            )

        instance = handle_callback(self.get_object(), request)

        return Response(FileSerializer(instance).data)
