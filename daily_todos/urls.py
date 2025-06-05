from django.urls import path

from daily_todos.views import live_todo, live_todo_key_list

urlpatterns = [
    path("live_todo/",live_todo_key_list),
    path("live_todo/<str:key>/",live_todo),
]
