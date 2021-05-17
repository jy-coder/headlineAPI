import os
import sys
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import django
django.setup()
from database.models import *




if __name__ == '__main__':
    catogries = ["all","Covid-19","singapore","world","business", "tech", "asia","life","sport", "opinion"]
    for category in catogries:
        category = Category(category_name=category)
        print("category saved to database")
        category.save()


