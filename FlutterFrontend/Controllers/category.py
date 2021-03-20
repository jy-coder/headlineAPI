from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from database.models import *
from firebase_admin import auth
from ..utils import *
from django.http import HttpResponse
from django.db.models import F
from datetime import datetime, timedelta
from django.forms.models import model_to_dict

@csrf_exempt
@require_http_methods(["GET"])
def category_count(req):
    # localhost:8000/count/?tabName=all_articles&category=world
    # localhost:8000/count/?tabName=daily_read
    user = authenticate(req)

    """
    count number of articles in each category of current date
    """
    tabName = ""
    articles_count = 0
    articles = []

    tabName = req.GET.get("tabName", None)
    category = req.GET.get("category", "all")
    if tabName == "all_articles":  
        if category != "all":
            articles = Article.objects.filter(category=category)  
        else:
            articles = Article.objects.all()
  

    elif user and tabName != "all_articles":
        if tabName =="daily_read":  
            articles= Recommend.objects.filter(user_id=user["user_id"])# always be up to date
        elif tabName == "History":
            articles = ReadingHistory.objects.filter(user_id=user["user_id"])
        elif tabName == "Saved":
            articles = Bookmark.objects.filter(user_id=user["user_id"]) # get all bookmark
 
    articles_count = len(articles)

    return jsonify({"count" : articles_count},status_code=200)


@csrf_exempt
@require_http_methods(["GET"])
def category(req):
    categories = list(Category.objects.values())
    return jsonify(categories, status_code=200)