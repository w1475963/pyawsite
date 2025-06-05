from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from daily_todos.serializer import LiveTodoSerializer
from .models import LiveTodo

@api_view(["GET"])
def live_todo_key_list(request):
    enabled_keys = LiveTodo.objects.filter(is_enabled=True).values_list('key', flat=True)
    
    key_list = list(enabled_keys)
    
    return Response(key_list)

@api_view(["GET"])
def live_todo(request,key):
    obj = get_object_or_404(LiveTodo, key=key)
    if request.method == "GET":
        serializer = LiveTodoSerializer(obj)
        return Response(serializer.data)
