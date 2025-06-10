from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import AdminLongTermToken
import time
import logging

logger = logging.getLogger(__name__)


class AdminLongTermTokenAuthentication(BaseAuthentication):
    """管理员长期Token认证类"""

    keyword = "LTToken"

    def authenticate(self, request):
        # 从请求头中提取Token
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        try:
            scheme, token = auth_header.split()
        except ValueError:
            raise AuthenticationFailed("无效的认证头格式")

        if scheme.lower() != self.keyword.lower():
            return None

        return self.authenticate_credentials(token, request)

    def authenticate_credentials(self, token, request):
        try:
            obj = AdminLongTermToken.objects.get(token=token)
        except AdminLongTermToken.DoesNotExist:
            raise AuthenticationFailed("Token无效")

        # 检查Token有效期
        if obj.expires_at and time.time() > obj.expires_at.timestamp():
            raise AuthenticationFailed("Token已过期")

        # 检查用户是否为管理员且激活状态
        if not obj.user.is_active or not obj.user.is_staff:
            raise AuthenticationFailed("用户权限不足")
        logger.info(
            f"管理员Token访问：{obj.user.username} from {request.META['REMOTE_ADDR']}"
        )

        return (obj.user, obj)
