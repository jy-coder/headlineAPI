import os
import sys
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import django
django.setup()
from database.models import *
from newsfetch.google import google_search
from newsfetch.news import newspaper
import requests
from bs4 import BeautifulSoup
import json

if __name__ == '__main__':
    # e.g saving to trend database
    # article = Trend(title="title",link="link",summary="summary",keywords="keywords",source="source")
    # article.save()
    print("hello")