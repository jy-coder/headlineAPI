
from django.db import models



class User(models.Model):
    user_id = models.AutoField(primary_key=True, unique=True)
    uuid = models.CharField(max_length =100, unique=True,default="")
    email = models.CharField(max_length=1000, unique=True)
    full_name = models.CharField(max_length=1000)

    class Meta:
        db_table = "User"
        index_together = [['email']]


class Article(models.Model):
    article_id = models.AutoField(primary_key=True, unique=True)
    title = models.CharField(max_length=1000, blank=True)
    link = models.CharField(max_length=1000, blank=True)
    summary = models.CharField(max_length=3000, blank=True)
    keywords = models.CharField(max_length=3000, blank=True)
    category = models.CharField(max_length=100, blank=True)
    source = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = "Article"


class ArticleCategory(models.Model):
    category_id = models.AutoField(primary_key=True, unique=True)
    category_name = models.CharField(max_length=100, blank=True)
    class Meta:
        db_table = "ArticleCategory"


class UserArticleCategory(models.Model):
    user_article_id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category =  models.ForeignKey(ArticleCategory,on_delete=models.CASCADE)
    class Meta:
        db_table = "UserArticleCategory"
