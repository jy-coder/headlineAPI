from django.urls import path
from . import api

urlpatterns = [
    path("test1", api.test1, name="test"),
    path("category", api.category, name="category"),

    path("register", api.register, name="register"),
    path("subscription", api.subscription, name="subscription"),
    path("user_subscription", api.user_subscription, name="user_subscription"),

    path("articles/", api.articles, name="articles"),
    path("article/", api.article, name="article"),
    path("history/", api.history, name="history"),
    path("bookmark/", api.bookmark, name="bookmark"),
    path("count/", api.category_count, name="count"),

    path("search_suggestion/", api.search_suggestion, name="search_suggestion"),
    path("search_result/", api.search_result, name="search_result"),

]