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
    subscription = list(Subscription.objects.filter(user_id=user["user_id"])\
        .select_related("category").values_list("category__category_name",flat=True))

    # get latest reading history category based on subscription
    if subscription:
        history_summary = list(ReadingHistory.objects.filter(user_id=user["user_id"]).select_related("article")\
            .values("article__category", "article__summary").annotate(summary=F('article__summary'))\
                .filter(article__category__in=subscription).values_list("summary",flat=True))

    # exclude current recommendation & reading history
    # if user read before, it will not appear in recommendation
    history = list(ReadingHistory.objects.filter(user_id=user["user_id"]).values_list("article_id", flat=True))
    recommendation = list(Recommend.objects.filter(user_id=user["user_id"]).values_list("article_id", flat=True))
    articles = Article.objects.exclude(article_id__in=recommendation).exclude(article_id__in=history)\
                .filter(category__in=subscription).values("summary","category","article_id")

    articles_summary = list(articles.values_list("summary",flat=True))
    article_id_list = list(articles.values_list("article_id",flat=True))

    for summary in history_summary:
        recommend_article_id_list = ds.calculate_similarity(summary,articles_summary,article_id_list)
   
    for recommend_article_id in recommend_article_id_list:
        recommend = Recommend(user_id=user["user_id"],article=article)
        # recommend.save()