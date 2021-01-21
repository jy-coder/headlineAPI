from django.urls import path
from . import api

urlpatterns = [
    path("test1", api.test1, name="test"),
]