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
    # localhost:8000/recommend/?date=Three%20Days&category=&site=
    user = authenticate(req)
    
    dateRange = req.GET.get("date", "")
    category_str = req.GET.get("category", "")
    site_str = req.GET.get("site", "")

    category = []
    site = []

    if category_str != "":
        category = string_to_list(category_str)
    if site != "":
        site = string_to_list(site_str)
    
    articles = []
    day = 0
  
    if dateRange == "One Day":
        day = 1
    elif dateRange == "Two Days":
        day = 2
    elif dateRange == "Three Days":
        day = 3
    elif dateRange == "Four Days":
        day = 4
    elif dateRange == "Five Days":
        day = 5
    elif dateRange == "Six Days":
        day = 6
    elif dateRange == "Seven Days":
        day = 7

    subscription = list(Subscription.objects.filter(user_id=user["user_id"])\
    .select_related("category").values_list("category__category_name",flat=True))


    recommends = Recommend.objects.filter(user_id=user["user_id"]).select_related('article')\
    .annotate(id=F('article__article_id'),title=F('article__title'),link=F('article__link'),summary=F('article__summary')\
    ,description=F('article__description'),image_url=F('article__image_url'),\
    category=F('article__category'),source=F('article__source'), publication_date=F('article__publication_date'), date=F('article__date')\
    ).filter(category__in=subscription).order_by("-publication_date").annotate(id=F('article_id'))

  

    if category_str != "" :
        recommends = recommends.filter(category__in=category)

    if dateRange != "":
        recommends = recommends.filter(publication_date__date=datetime.now()-timedelta(days=day))

    if site_str != "":
        recommends = recommends.filter(source__in=site)


    recommends = list(recommends.values())

    return jsonify(recommends,status_code=200)


@csrf_exempt
@require_http_methods(["GET"])
def trend(req):
    # localhost:8000/trend
    user = authenticate(req)

    articles = Likes.objects.select_related('article').values('article_id', 'article__article_id')\
        .annotate(dcount=Count('article__article_id')).annotate(count=F('dcount'),title=F('article__title'),link=F('article__link'),summary=F('article__summary')\
    ,description=F('article__description'),image_url=F('article__image_url'),id=F('article_id'),\
    category=F('article__category'),source=F('article__source'), publication_date=F('article__publication_date'), date=F('article__date')).order_by('-dcount')

    
    if user:
        subscription = list(Subscription.objects.filter(user_id=user["user_id"])\
        .select_related("category").values_list("category__category_name",flat=True))

        articles = articles.filter(category__in=subscription)


    return jsonify(list(articles),status_code=200)

