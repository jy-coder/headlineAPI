from django.urls import path
from . import api

urlpatterns = [
    path("test1", api.test1, name="test"),
    path("category", api.category, name="category"),

    path("register", api.register, name="register"),
    path("subscription", api.subscription, name="subscription"),

    path("article/", api.article, name="article"),
    path("history/", api.history, name="history")

]