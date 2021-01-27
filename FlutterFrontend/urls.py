from django.urls import path
from . import api

urlpatterns = [
    path("test1", api.test1, name="test"),
    path("category", api.category, name="category"),

    path("register", api.register, name="register"),
    path("set_category", api.set_category, name="set_category")
]