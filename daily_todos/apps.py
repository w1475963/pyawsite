from django.apps import AppConfig


class DailyTodosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField' # pyright: ignore[reportAssignmentType]
    name = 'daily_todos'
