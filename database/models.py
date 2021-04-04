
from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True, unique=True)
    uuid = models.CharField(max_length =100, unique=True,default="")
    email = models.CharField(max_length=1000, unique=True)
    full_name = models.CharField(max_length=1000)
    last_active = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        db_table = "User"
        index_together = [['email']]


class Article(models.Model):
    article_id = models.AutoField(primary_key=True, unique=True)
    title = models.CharField(max_length=1000, blank=True)
    link = models.CharField(max_length=1000, blank=True, unique=True)
    summary = models.CharField(max_length=3000, blank=True)
    description = models.TextField( blank=True)
    image_url = models.TextField( blank=True)
    keywords = models.CharField(max_length=3000, blank=True)
    category = models.CharField(max_length=100, blank=True)
    source = models.CharField(max_length=100, blank=True)
    publication_date = models.DateTimeField(auto_now_add=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        db_table = "Article"

class Category(models.Model):
    category_id = models.AutoField(primary_key=True, unique=True)
    category_name = models.CharField(max_length=100, blank=True)
    class Meta:
        db_table = "Category"


class Subscription(models.Model):
    subscription_id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category =  models.ForeignKey(Category,on_delete=models.CASCADE)
    class Meta:
        db_table = "Subscription"
        unique_together = (('user', 'category'),)

class ReadingHistory(models.Model):
    history_id = models.AutoField(primary_key=True, unique=True)
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    history_date = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        db_table = "ReadingHistory"
        unique_together = (('user', 'article'),)

class Bookmark(models.Model):
    bookmark_id = models.AutoField(primary_key=True, unique=True)
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        db_table = "Bookmark"
        unique_together = (('user', 'article'),)

class Recommend(models.Model):
    recommend_id = models.AutoField(primary_key=True, unique=True)
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    recommend_date = models.DateTimeField(auto_now_add=True, blank=True)
    similar_headline = models.CharField(max_length=1000, blank=True)
    similarity = models.IntegerField(default=0, blank=True)
    history = models.ForeignKey(Article,on_delete=models.CASCADE,null=True,related_name="history")
    class Meta:
        db_table = "Recommend"
        unique_together = (('user', 'article'),)

class Trend(models.Model):
    article_id = models.AutoField(primary_key=True, unique=True)
    title = models.CharField(max_length=1000, blank=True)
    link = models.CharField(max_length=1000, blank=True)
    summary = models.CharField(max_length=3000, blank=True)
    description = models.TextField( blank=True)
    image_url = models.TextField( blank=True)
    keywords = models.CharField(max_length=3000, blank=True)
    category = models.CharField(max_length=100, blank=True)
    source = models.CharField(max_length=100, blank=True)
    publication_date = models.DateTimeField(auto_now_add=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    class Meta:
        db_table = "Trend"

class RelatedArticle(models.Model):
    related_id = models.AutoField(primary_key=True, unique=True)
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
    title = models.CharField(max_length=1000, blank=True)
    link = models.CharField(max_length=1000, blank=True)
    summary = models.CharField(max_length=3000, blank=True)
    description = models.TextField( blank=True)
    image_url = models.TextField( blank=True)
    keywords = models.CharField(max_length=3000, blank=True)
    category = models.CharField(max_length=100, blank=True)
    source = models.CharField(max_length=100, blank=True)
    publication_date = models.DateTimeField(auto_now_add=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    class Meta:
        db_table = "RelatedArticle"

class NotInterested(models.Model):
    ni_id = models.AutoField(primary_key=True, unique=True)
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        db_table = "NotInterested"
        unique_together = (('user', 'article'),)


class NewsSite(models.Model):
    site_id = models.AutoField(primary_key=True, unique=True)
    site_name = models.CharField(max_length=100, blank=True)
    class Meta:
        db_table = "NewsSite"

class SiteSubscription(models.Model):
    site_subscription_id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    site =  models.ForeignKey(NewsSite,on_delete=models.CASCADE)
    class Meta:
        db_table = "SiteSubscription"
        unique_together = (('user', 'site'),)