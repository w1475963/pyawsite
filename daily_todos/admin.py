from uuid import uuid4
from django.contrib import admin
from . import models

def copy_selected_objects(modeladmin, request, queryset):
    for obj in queryset:
        if hasattr(obj,"key"):
            obj.key = uuid4()
        if hasattr(obj,"name"):
            obj.name = obj.name + "(copied)"
        obj.pk = None  # 生成新ID
        obj.save()
    modeladmin.message_user(request, f"成功拷贝 {queryset.count()} 条记录")

copy_selected_objects.short_description = "拷贝选中的记录"  # pyright: ignore[reportFunctionMemberAccess] 

def generate_new_key(modeladmin, request, queryset):
    counter = 0
    for obj in queryset:
        if hasattr(obj,"key"):
            obj.key = uuid4()
            counter += 1
        obj.save()
    modeladmin.message_user(request, f"成功更改 {counter} 条记录 (共 {queryset.count()})")
generate_new_key.short_description = "更新key"  # pyright: ignore[reportFunctionMemberAccess] 

# Register your models here.
@admin.register(models.LiveTodo)
class LiveTodoAdmin(admin.ModelAdmin):
    actions = [copy_selected_objects,generate_new_key]  # 为LiveTodo模型启用拷贝动作
    list_display = ["name", "is_enabled", "start_time", "level" ]

@admin.register(models.DateTodos)
class DateTodosAdmin(admin.ModelAdmin):
    actions = [copy_selected_objects,generate_new_key]  # 为LiveTodo模型启用拷贝动作
    list_display = ["name", "date" ]

