from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from database.models import *
from firebase_admin import auth
from ..utils import *
from django.http import HttpResponse
from django.db.models import F
from datetime import datetime, timedelta
from django.forms.models import model_to_dict
from django.db.models import Count

@csrf_exempt
@require_http_methods(["GET"])
def articles(req):
    user = authenticate(req)
    
    page_type = req.GET.get("type", "all_articles")
    category= req.GET.get("category", "all")
  
    # localhost:8000/article/?type=all_articles
    if page_type == "all_articles":
        if category == "all":
            articles =  Article.objects.order_by("-article_id").annotate(id=F('article_id'))
        else:
            articles =  Article.objects.filter(category=category).order_by("-article_id").annotate(id=F('article_id'))
      

    return jsonify(list(articles.values())[:50],status_code=200)


@csrf_exempt
@require_http_methods(["GET"])
def article(req):   
    # localhost:8000/article/?article_id=46&category=world&tabName=all_articles&index=1
    article = {} # change this
    article_id = req.GET.get("article_id", None)
    category = req.GET.get("category", None)
    tabName = req.GET.get("tabName", None)
    ind = req.GET.get("index", None)

    
    if ind:
        if tabName == "all_articles" :
            model_obj = Article.objects
        elif tabName == "reading_list":
            model_obj = Bookmark.objects
    

        if category == "all":
            article = model_obj.order_by("-article_id")
        elif category != "all":
            article = model_obj.filter(category=category, publication_date__gte=current_date).order_by("-article_id")

        if int(ind) <= len(article) - 1:
            article = list(article.values())[int(ind)]
            article["id"] = article["article_id"]

        else:
            return jsonify({},status_code=200)

    
    return jsonify(article,status_code=200)

@csrf_exempt
@require_http_methods(["GET"])
def count(req):
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
def recommend(req):
    # localhost:8000/recommend
    user = authenticate(req)
    articles = []

    subscription = list(Subscription.objects.filter(user_id=10)\
    .select_related("category").values_list("category__category_name",flat=True))

    articles = Recommend.objects.filter(user_id=10).select_related('article')\
        .annotate(id=F('article__article_id'),title=F('article__title'),link=F('article__link'),summary=F('article__summary')\
        ,description=F('article__description'),image_url=F('article__image_url'),\
        category=F('article__category'),source=F('article__source'), publication_date=F('article__publication_date'), date=F('article__date')\
    ).filter(category__in=subscription).values("article_id","title", "link", 
    "summary", "description", "image_url", 
    "category", "source", "publication_date", "date").annotate(id=F('article_id'))
    articles = list(articles.values())

    return jsonify(articles,status_code=200)


@csrf_exempt
@require_http_methods(["GET"])
def trend(req):
    # localhost:8000/trend
    trend_articles_id = ReadingHistory.objects.values("article_id").annotate(dcount=Count('article_id'))\
        .order_by('-dcount').values_list('article_id', flat=True)[:5]
    articles = Article.objects.filter(article_id__in=trend_articles_id)
    articles = list(articles.values().annotate(id=F('article_id')))

    return jsonify(articles,status_code=200)

