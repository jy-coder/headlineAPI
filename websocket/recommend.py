from database.models import *
from gensim.models.keyedvectors import KeyedVectors
from datetime import datetime, timedelta
from django.db.models import F
import gensim.downloader as api
model_path = api.load("word2vec-google-news-300", return_path=True)
w2v_model = KeyedVectors.load_word2vec_format(model_path, binary=True,limit=10000)
from .utils.DocSim import DocSim
ds = DocSim(w2v_model)


def update_recommend(email):
    user = User.objects.get(email=email)
    user_id = 0

    if not user:
        return

    # get user subscription
    subscription = list(Subscription.objects.filter(user_id=user.user_id)\
        .select_related("category").values_list("category__category_name",flat=True))

    # get latest reading history category based on subscription
    if subscription:
        history = ReadingHistory.objects.filter(user_id=user.user_id).select_related("article")\
            .values("article__category", "article__summary","article__article_id").annotate(summary=F('article__summary'),id=F("article__article_id"))\
                .filter(article__category__in=subscription)
        history_summary = list(history.values_list("summary",flat=True))
        similar_to_article = list(history.values_list("id",flat=True))

    # exclude current recommendation & reading history
    # if user read before, it will not appear in recommendation
    history = list(ReadingHistory.objects.filter(user_id=user.user_id).values_list("article_id", flat=True))
    recommendation = list(Recommend.objects.filter(user_id=user.user_id).values_list("article_id", flat=True))
    articles = Article.objects.exclude(article_id__in=recommendation).exclude(article_id__in=history)\
                .filter(category__in=subscription).values("summary","category","article_id","title")

    articles_summary = list(articles.values_list("summary",flat=True))
    article_id_list = list(articles.values_list("article_id",flat=True))
    headline = list(articles.values_list("title",flat=True))

    for ind, summary in enumerate(history_summary):
        recommend_articles = ds.calculate_similarity(summary,articles_summary,article_id_list,headline)
        for recommend_article in recommend_articles:
            try:
                similar_headline = Article.objects.get(article_id=similar_to_article[ind]).title
                recommend = Recommend(user_id=user.user_id,article_id=recommend_article['id'], \
                    similar_headline=similar_headline,similarity=recommend_article["similarity"])
                recommend.save()
                print("successfully save recommend to database")
            except Exception as e:
                pass
                # print(e)