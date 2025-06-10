from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User

class AdminLongTermToken(models.Model):
    """管理员长期有效Token模型"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="关联用户",
        limit_choices_to={"is_staff": True}, 
    )
    token = models.CharField(
        max_length=64,
        unique=True,
        verbose_name="Token值",
        help_text="自动生成的唯一令牌",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="过期时间",
        help_text="可选：设置后Token将在此时效后失效",
    )
    description = models.CharField(max_length=200, blank=True, verbose_name="备注")

    def generate_token(self):
        """生成UUID格式的Token"""
        self.token = str(uuid4()).replace("-", "")
        return self.token

    def save(self, *args, **kwargs):
        if not self.token:
            self.generate_token()  # 首次保存时自动生成Token
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}的Token"

    class Meta:
        verbose_name = "管理员长期Token"
        verbose_name_plural = "管理员长期Tokens"
