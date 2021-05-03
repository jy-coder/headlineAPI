import os
import sys
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import django
django.setup()
from database.models import *




if __name__ == '__main__':
    # catogries = ["all","world","business","asia","singapore", "life","covid19", "tech", "opinion", "sport"]
    record = [
    { 
    "adv_category":"business", 
    "img_link":"https://scontent-xsp1-3.xx.fbcdn.net/v/t1.6435-9/167274276_3751944718257007_7896160353438881870_n.png?_nc_cat=111&ccb=1-3&_nc_sid=6e5ad9&_nc_ohc=Tm_4wDtKSm4AX-f7rYC&_nc_ht=scontent-xsp1-3.xx&oh=7e9079ad6db09dc19be635e346873207&oe=60B509FD",
    "web_link":"https://www.foodpanda.sg/"
    }]


    for r in record:
        ad = Advertisement(
        adv_category=r["adv_category"], 
        img_link=r["img_link"],
        web_link=r["web_link"]
        )
        print("ads saved to database")
        ad.save()


