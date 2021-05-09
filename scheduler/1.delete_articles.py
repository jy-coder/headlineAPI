import os
import sys
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import django
django.setup()
from datetime import datetime, timedelta
from database.models import *


if __name__ == '__main__':
    articles = Article.objects.filter(publication_date__lte=datetime.today() - timedelta(days=7))
    articles.delete()