from database.models import *
from gensim.models.keyedvectors import KeyedVectors
from datetime import datetime, timedelta
from django.db.models import F
import gensim.downloader as api
model_path = api.load("word2vec-google-news-300", return_path=True)
w2v_model = KeyedVectors.load_word2vec_format(model_path, binary=True,limit=10000)
from .utils.DocSim import DocSim
from time import sleep
ds = DocSim(w2v_model)


def compare_headline(user, target_article_id):
    target_headline= Article.objects.get(article_id=target_article_id).title
    not_interested = NotInterested.objects.filter(user_id=user.user_id).select_related("article")\
            .values("article__title","article__article_id").annotate(title=F('article__title'),id=F("article__article_id"))
    title = list(not_interested .values_list("title",flat=True))
    similar = ds.calculate_similarity_r(target_headline,title)
    return similar


def reload_not_interested(user):
    recommends = Recommend.objects.filter(user_id=user.user_id).select_related("article")\
        .values("article__title","article__article_id").annotate(title=F('article__title'),id=F("article__article_id"))
    not_interested = NotInterested.objects.filter(user_id=user.user_id).select_related("article")\
        .values("article__title","article__article_id").annotate(title=F('article__title'),id=F("article__article_id"))
    title = list(not_interested .values_list("title",flat=True))
    for recommend in recommends:
        target_headline= Article.objects.get(article_id=recommend["id"]).title
        similar = ds.calculate_similarity_r(target_headline,title)
        if similar:
            Article.objects.get(article_id=recommend["id"]).delete()




def update_recommend(email):
    user = User.objects.get(email=email)
    reload_not_interested(user)

    if not user:
        return

    # get user subscription
    subscription = list(Subscription.objects.filter(user_id=user.user_id)\
        .select_related("category").values_list("category__category_name",flat=True))

    # get latest reading history category based on subscription
    if subscription:
        history = ReadingHistory.objects.filter(user_id=user.user_id).select_related("article")\
            .values("article__category", "article__summary","article__article_id").annotate(summary=F('article__summary'),id=F("article__article_id"), category=F("article__category"))\
                .filter(article__category__in=subscription)
        history_summary = list(history.values_list("summary",flat=True))
        similar_to_article = list(history.values_list("id",flat=True))
        history_category = list(history.values_list("category",flat=True)) 

    not_interested = list(NotInterested.objects.filter(user_id=user.user_id).values_list("article_id" ,flat=True))

    # exclude current recommendation & reading history
    # if user read before, it will not appear in recommendation
    history = list(ReadingHistory.objects.filter(user_id=user.user_id).values_list("article_id", flat=True))
    recommendation = list(Recommend.objects.filter(user_id=user.user_id).values_list("article_id", flat=True))
    articles = Article.objects.exclude(article_id__in=recommendation).exclude(article_id__in=history).exclude(article_id__in=not_interested)\
                .filter(category__in=subscription).values("summary","category","article_id","title")

    articles_summary = list(articles.values_list("summary",flat=True))
    article_id_list = list(articles.values_list("article_id",flat=True))
    headline = list(articles.values_list("title",flat=True))


    for ind, summary in enumerate(history_summary):
        recommend_articles = ds.calculate_similarity(summary,articles_summary,article_id_list,headline)
        for recommend_article in recommend_articles:
            try:
                similar_headline = Article.objects.get(article_id=similar_to_article[ind]).title
                similar_category = Article.objects.get(article_id=similar_to_article[ind]).category
                if (similar_category == history_category[ind]):
                    similar = compare_headline(user,recommend_article['id'])
                    if not similar:
                        recommend = Recommend(user_id=user.user_id,article_id=recommend_article['id'], \
                            similar_headline=similar_headline,similarity=recommend_article["similarity"], similar_id=similar_to_article[ind])
                        recommend.save()
                        print("successfully save recommend to database")
                        
            except Exception as e:
                pass
                print(e)