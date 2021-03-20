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
      
    elif page_type == "daily_read":
        if category == "all":
                articles = Recommend.objects.filter(user_id=user["user_id"]).select_related('article')\
                .annotate(id=F('article__article_id'),title=F('article__title'),link=F('article__link'),summary=F('article__summary')\
                ,description=F('article__description'),image_url=F('article__image_url'),\
                category=F('article__category'),source=F('article__source'), publication_date=F('article__publication_date'), date=F('article__date')\
            ).values("article_id","title", "link", 
            "summary", "description", "image_url", 
            "category", "source", "publication_date", "date")

        else:
            articles = Recommend.objects.filter(user_id=user["user_id"]).select_related('article').filter(article__category=category)\
                    .annotate(id=F('article__article_id'),title=F('article__title'),link=F('article__link'),summary=F('article__summary')\
                    ,description=F('article__description'),image_url=F('article__image_url'),\
                    category=F('article__category'),source=F('article__source'), publication_date=F('article__publication_date'), date=F('article__date')\
            ).values("article_id","title", "link", 
            "summary", "description", "image_url", 
            "category", "source", "publication_date", "date")
   
    return jsonify(list(articles.values())[:50],status_code=200)


@csrf_exempt
@require_http_methods(["GET"])
def article(req):
    user = authenticate(req)
    
    # localhost:8000/article/?article_id=46&category=world&tabName=all_articles&index=1
    article = {}
    current_date = (datetime.now()-timedelta(days=14)).strftime("%Y-%m-%d") # change this
    article_id = req.GET.get("article_id", None)
    category = req.GET.get("category", None)
    tabName = req.GET.get("tabName", None)
    ind = req.GET.get("index", None)

    
    if ind:
        if tabName == "all_articles" :
            model_obj = Article.objects
        elif tabName == "reading_list":
            model_obj = Bookmark.objects
        elif tabName == "daily_read":
            model_obj = Recommend.objects
    

        if category == "all":
            article = model_obj.filter( publication_date__gte=current_date).order_by("-article_id")
        elif category != "all":
            article = model_obj.filter(category=category, publication_date__gte=current_date).order_by("-article_id")

        if int(ind) <= len(article) - 1:
            article = list(article.values())[int(ind)]
            article["id"] = article["article_id"]

        else:
            return jsonify({},status_code=200)

    
    return jsonify(article,status_code=200)