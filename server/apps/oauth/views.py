from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User
from zq_django_util.exceptions import ApiException
from zq_django_util.response import ResponseType

from .serializers import (
    OpenIdLoginSerializer,
    UnionIdLoginSerializer,
    WechatLoginSerializer,
    ZqAuthLoginSerializer,
)


class OpenIdLoginView(TokenObtainPairView):
    """
    open id 登录视图（仅供测试微信登录使用）
    """

    queryset = User.objects.all()
    serializer_class = OpenIdLoginSerializer

    def post(self, request, *args, **kwargs):
        """
        增加 post 方法, 支持 open id 登录
        """
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError:
            raise ApiException(
                ResponseType.ThirdLoginFailed,
                msg="微信登录失败",
                detail="生成token时simple jwt发生TokenError",
                record=True,
            )

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class WechatLoginView(OpenIdLoginView):
    """
    微信登录视图
    """

    queryset = User.objects.all()
    serializer_class = WechatLoginSerializer


class UnionIdLoginView(TokenObtainPairView):
    """
    zq auth union id 登录视图
    """

    queryset = User.objects.all()
    serializer_class = UnionIdLoginSerializer

    def post(self, request, *args, **kwargs):
        """
        增加 post 方法, 支持 sso 登录
        """
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError:
            raise ApiException(
                ResponseType.ThirdLoginFailed,
                msg="自强账号登录失败",
                detail="生成token时simple jwt发生TokenError",
                record=True,
            )

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class ZqAuthLoginView(UnionIdLoginView):
    """
    zq auth 登录视图
    """

    serializer_class = ZqAuthLoginSerializer
