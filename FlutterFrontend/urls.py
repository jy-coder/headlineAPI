from django.urls import path
from . import api
from .Controllers import article, category,search, authenticate, subscription, activity

urlpatterns = [
    path("test1", api.test1, name="test"),

    path("category", category.category, name="category"),
    path("count/",article.count, name="count"),

    path("register", authenticate.register, name="register"),

    path("articles/", article.articles, name="articles"),
    path("article/", article.article, name="article"),

    path("recommend/", article.recommend, name="recommend"),
    path("trend/", article.trend, name="trend"),

    path("subscription", subscription.subscription, name="subscription"),
    path("user_subscription", subscription.user_subscription, name="user_subscription"),

    path("history/", activity.history, name="history"),
    path("bookmark/", activity.bookmark, name="bookmark"),
    
    path("search_suggestion/", search.search_suggestion, name="search_suggestion"),
    path("search_result/", search.search_result, name="search_result"),

]