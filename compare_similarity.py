# https://github.com/v1shwa/document-similarity

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import django
django.setup()
from database.models import *
from gensim.models.keyedvectors import KeyedVectors
from datetime import datetime, timedelta
from django.db.models import F
model_path = './data/GoogleNews-vectors-negative300.bin'
w2v_model = KeyedVectors.load_word2vec_format(model_path, binary=True)
from DocSim import DocSim
ds = DocSim(w2v_model)


if __name__ == '__main__':
    time_gte= datetime.now() - timedelta(days=1)
    today_date = datetime.now().strftime("%Y-%m-%d")

    user_id_list = list(User.objects.values_list("user_id",flat=True))

    # TODO get user who are currently active (not by logged in)



    # TODO set time interval
    # update at setted time interval for each user
    for user_id in user_id_list:
        recommend_article_id_list = []
        reading_history = ReadingHistory.objects.filter(user_id=user_id)
        reading_history = list(reading_history.annotate(category=F('article__category')).order_by("-history_id").values("article_id","user_id", "category"))[:5]
   

        for rh in reading_history:
            rh_temp = list(Article.objects.filter(article_id=rh["article_id"]).values("summary"))[0]
            articles = Article.objects.filter(date__lte=datetime.now(),date__gte=time_gte,category=rh["category"]).exclude(article_id = rh["article_id"])
            articles = list(articles.values_list("summary",flat=True))
            article_id_list = list(Article.objects.values_list("article_id",flat=True))
        
            recommend_article_id_list  = ds.calculate_similarity(rh_temp["summary"], articles,article_id_list)

        
            for recommend_article_id in recommend_article_id_list:
                user= User.objects.get(user_id=user_id)
                article = Article.objects.get(article_id=recommend_article_id)
                try:
                    recommend = Recommend(user=user,article=article)
                    recommend.save()
                    print(f"Article ID :{recommend_article_id} recommend to User ID:{user_id}")
                    print("===========================================================================")
                except Exception as e:
                    print(e)                





   


