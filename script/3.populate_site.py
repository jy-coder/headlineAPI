import os
import sys
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import django
django.setup()
from database.models import *


if __name__ == '__main__':
    sites = ["The Straits Times","Channel News Asia", "CNBC", "New York Daily News", "The Guardian",\
    "Yahoo News","Foxnews","New York Post","Vox","The New York Times",
    "The Independent","The Online Citizen","Mothership","Asiaone"]
    for site in sites:
        site = NewsSite(site_name=site)
        site.save()
        print("site saved to database")


