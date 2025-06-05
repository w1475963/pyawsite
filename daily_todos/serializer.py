from .models import LiveTodo, DateTodos
from rest_framework.serializers import ModelSerializer

class LiveTodoSerializer(ModelSerializer):
    class Meta:
        model = LiveTodo
        fields = "__all__"

class DateTodosSerializer(ModelSerializer):
    class Meta:
        model = DateTodos
        fields = "__all__"
