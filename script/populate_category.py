import os
import sys
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import django
django.setup()
from database.models import *




if __name__ == '__main__':
    catogries = ["all","tech", "multimedia", "world", "business", "sport", "life", "opinion", "asia"]
    for category in catogries:
        category = Category(category_name=category)
        print("category saved to database")
        category.save()


