from django.urls import path
from .views import ws_update
urlpatterns = [
    path("ws_update",ws_update)
]
