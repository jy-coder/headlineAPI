from django.urls import path
from . import api
from .Controllers import article, category,search, user, subscription, activity,site

urlpatterns = [
    path("test1", api.test1, name="test"),

    path("category", category.category, name="category"),
    path("count/",article.count, name="count"),

    path("register", user.register, name="register"),
    path("last_active", user.last_active, name="last_active"),

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


    path("bookmark_article_ids/", activity.bookmark_article_ids , name="bookmark_article_ids"),

    path("sites", site.sites , name="sites"),
    path("site_subscription",site.site_subscription,name="site_subscription"),

    path("like/", activity.like_article, name="like"),
    path("like_article_ids/", activity.like_article_ids, name="activity.like_article_ids"),

    path("not_interested/", activity.not_interested, name="not_interested"),

    path("related/", article.related_article, name="related"),

]