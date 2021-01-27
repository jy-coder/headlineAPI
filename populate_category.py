import os
# django project name is adleads, replace adleads with your project name
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import django
django.setup()
from database.models import *




if __name__ == '__main__':
    catogries = ["tech", "multimedia", "world", "business", "sport", "life", "opinion", "asia", "all"]
    for category in catogries:
        category = ArticleCategory(category_name=category)
        category.save()


