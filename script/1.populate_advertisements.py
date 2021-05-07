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
    },
     { 
    "adv_category":"business", 
    "img_link":"https://tpc.googlesyndication.com/simgad/15761416798645073563",
    "web_link":"https://www.gevme.com/thepeakgolf2021"
    },
    { 
    "adv_category":"life", 
    "img_link":"https://tpc.googlesyndication.com/simgad/462633356773186180?sqp=4sqPyQQ7QjkqNxABHQAAtEIgASgBMAk4A0DwkwlYAWBfcAKAAQGIAQGdAQAAgD-oAQGwAYCt4gS4AV_FAS2ynT4&rs=AOga4ql52CEFd6ScPy2LG7DOiYerlhHkHQ",
    "web_link":"https://kidchamp.sg/?gclid=EAIaIQobChMI9pjOoO6t8AIVAlyPCh0sGQ1lEAEYASAAEgKc-_D_BwE"
    },
    {
    "adv_category":"tech",
    "img_link":"https://tpc.googlesyndication.com/simgad/11113741218405610751?sqp=4sqPyQQ7QjkqNxABHQAAtEIgASgBMAk4A0DwkwlYAWBfcAKAAQGIAQGdAQAAgD-oAQGwAYCt4gS4AV_FAS2ynT4&rs=AOga4qnV0o5t7w2MotsFJVLjy8w668cmKw",
    "web_link":"https://www.lenovo.com/sg/en/laptops/thinkpad/thinkpad-x1/X1-Carbon-G9/p/22TP2X1X1C9?cid=sg:display|se|google|prospecting-boost|aamsmb|||12873339337|130077451908||display_standard|nonbrand|all&gclid=EAIaIQobChMIufXM6-2t8AIV5Fh8Ch21Vgg1EAEYASAAEgL0nvD_BwE"
    },
    {
    "adv_category":"tech",
    "img_link":"https://tpc.googlesyndication.com/simgad/14492244499578975378?sqp=4sqPyQQ7QjkqNxABHQAAtEIgASgBMAk4A0DwkwlYAWBfcAKAAQGIAQGdAQAAgD-oAQGwAYCt4gS4AV_FAS2ynT4&rs=AOga4qkxRVp4hf0vPJyDvDjwF9raw2EyjQ",
    "web_link":"https://www.winmate.com/ProductCategory/Detail/ATEX_Grade_Panel_PC?gclid=EAIaIQobChMIisK8yu6t8AIV7S-3AB3tJwJ2EAEYASAAEgIR-fD_BwE"
    }
    ]


    for r in record:
        ad = Advertisement(
        adv_category=r["adv_category"], 
        img_link=r["img_link"],
        web_link=r["web_link"]
        )
        print("ads saved to database")
        ad.save()