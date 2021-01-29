# https://github.com/v1shwa/document-similarity

import os
# django project name is adleads, replace adleads with your project name
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import django
django.setup()
from database.models import *
from gensim.models.keyedvectors import KeyedVectors
model_path = './data/GoogleNews-vectors-negative300.bin'
w2v_model = KeyedVectors.load_word2vec_format(model_path, binary=True)
from DocSim import DocSim
ds = DocSim(w2v_model)


if __name__ == '__main__':
    articles = list(Article.objects.values_list("summary",flat=True))
    article_id_list = list(Article.objects.values_list("id",flat=True))
   
    sim_scores = ds.calculate_similarity(articles[0], articles[1:],article_id_list)
    print(sim_scores)
    # print("hello")




