from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(["POST"])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(request, username=username, password=password)

    if user:
        # 1. 设置会话Cookie（传统登录）
        login(request, user)  # 自动生成sessionid Cookie

        # 2. 生成JWT令牌（用于API）
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "message": "登录成功",
                "session_cookie_set": True,
                "tokens": {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
            }
        )
    return Response({"error": "认证失败"}, status=400)


@api_view(["POST"])
@permission_classes([AllowAny])  # 允许未认证用户访问
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(
            {"message": "用户注册成功", "user": serializer.data},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
