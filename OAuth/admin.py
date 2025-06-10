from django.contrib import admin
from .models import AdminLongTermToken


@admin.register(AdminLongTermToken)
class AdminLongTermTokenAdmin(admin.ModelAdmin):
    list_display = ["user", "token_short", "created_at", "expires_at", "description"]
    search_fields = ["user__username", "token"]
    actions = ["regenerate_token"]  # 添加生成新Token的动作

    def token_short(self, obj):
        """缩短Token显示长度"""
        return obj.token[:8] + "..."

    token_short.short_description = "Token"

    def regenerate_token(self, request, queryset):
        """批量重新生成Token"""
        for obj in queryset:
            obj.generate_token()
            obj.save()
        self.message_user(request, f"成功为{queryset.count()}个Token重新生成令牌")

    regenerate_token.short_description = "重新生成Token"

    fieldsets = (
        (None, {"fields": ("user", "description")}),
        ("Token设置", {"fields": ("expires_at",)}),
    )
    readonly_fields = ["token"]  # 禁止手动修改Token值
