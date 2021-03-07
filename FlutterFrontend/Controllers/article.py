from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from database.models import *
from firebase_admin import auth
from ..utils import *
from django.http import HttpResponse
from django.db.models import F
from datetime import datetime, timedelta
from django.forms.models import model_to_dict



# initialize_firebase()


@csrf_exempt
@require_http_methods(["GET"])
def articles(req):
    # user = authenticate(req)
    # email = user["email"]
    email = "test3@test.com"
    user = retrieve_user(email)

    itemsPerPage = 2
    page = req.GET.get("page", 1)
    page = int(page)
    start = (page - 1) * itemsPerPage
    end = page * itemsPerPage


    # either daily_read or all_articles
    page_type = req.GET.get("type", "all_articles")
    category = req.GET.get("category", "all")

    if category != "all":
        # localhost:8000/article/?page=1
        # localhost:8000/article/?page=2&category=business
        # localhost:8000/article/?page=3&category=all
        if page_type == "all_articles":
            articles = Article.objects.filter(category=category) 
        # localhost:8000/article/?page=2&category=business&type=daily_read
        # localhost:8000/article/?page=1&category=all&type=daily_read
        elif page_type == "daily_read":
            articles = Recommend.objects.select_related('article').filter(article__category=category)\
                .annotate(id=F('article__article_id'),title=F('article__title'),link=F('article__link'),summary=F('article__summary')\
                ,description=F('article__description'),image_url=F('article__image_url'),\
                category=F('article__category'),source=F('article__source'), publication_date=F('article__publication_date'), date=F('article__date')\
        ).values("article_id","title", "link", 
        "summary", "description", "image_url", 
        "category", "source", "publication_date", "date")

    else:
        if page_type == "all_articles":
            articles = Article.objects.all()
        elif page_type == "daily_read": 
            articles = Recommend.objects.filter(user=user).annotate(id=F('article__article_id'),title=F('article__title'),link=F('article__link'),summary=F('article__summary')\
                ,description=F('article__description'),image_url=F('article__image_url'),\
                category=F('article__category'),source=F('article__source'), publication_date=F('article__publication_date'), date=F('article__date')\
        ).values("article_id","title", "link", 
        "summary", "description", "image_url", 
        "category", "source", "publication_date", "date")

    if user:
        bookmarks_id_list = list(Bookmark.objects.filter(user=user).values_list("article__article_id",flat=True))
        articles = articles.exclude(article_id__in=bookmarks_id_list) # exclude bookmark
      

    articles = articles.order_by("-publication_date")[start:end].annotate(id=F('article_id'))
    articles = list(articles.values())
  
  
    return jsonify(articles,status_code=200)


@csrf_exempt
@require_http_methods(["GET"])
def article(req):
    email = "test3@test.com"
    user = retrieve_user(email)
    
    # localhost:8000/article/?article_id=46&category=world&tabName=all_articles&index=1
    article = []
    current_date = (datetime.now()-timedelta(days=14)).strftime("%Y-%m-%d") # change this
    article_id = req.GET.get("article_id", None)
    category = req.GET.get("category", None)
    tabName = req.GET.get("tabName", None)
    ind = req.GET.get("index", None)

    

    if tabName == "all_articles" and ind:
        if category == "all":
            article = Article.objects.filter( publication_date__gte=current_date).order_by("-article_id")
        

        elif category != "all":
            article = Article.objects.filter(category=category, publication_date__gte=current_date).order_by("-article_id")
            
        if user:
            bookmarks_id_list = list(Bookmark.objects.filter(user=user).values_list("article__article_id",flat=True)) 
            article = article.exclude(article_id__in=bookmarks_id_list) # exclude bookmark


        if int(ind) <= len(article) - 1:
            article = list(article.values())[int(ind)]
            article["id"] = article["article_id"]

        else:
            return jsonify({},status_code=200)

    
    return jsonify(article,status_code=200)