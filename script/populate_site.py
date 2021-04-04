import os
import sys
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import django
django.setup()
from database.models import *


if __name__ == '__main__':
    sites = ["The Straits Times","Channel News Asia", "CNBC", "New York Daily News", "business"]
    for site in sites:
        site = NewsSite(site_name=site)
        print("site saved to database")
        site.save()


