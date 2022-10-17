from django.urls import path
from .views import (
    TestCore,
)

app_name = "core"
urlpatterns = [
    path("", TestCore.as_view(), name="test"),
]
