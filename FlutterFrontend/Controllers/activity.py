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
@require_http_methods(["GET","POST"])
def history(req):
    user = authenticate(req)
    history = []
    date = req.GET.get("date", None)
    if(req.method == "GET"):
        history = ReadingHistory.objects.filter(user_id=user["user_id"]).select_related('article')\
                .annotate(id=F('article__article_id'),title=F('article__title'),link=F('article__link'),summary=F('article__summary')\
                ,description=F('article__description'),image_url=F('article__image_url'),\
                category=F('article__category'),source=F('article__source'), publication_date=F('article__publication_date'), date=F('article__date')\
        ).values("id","title", "link", 
        "summary", "description", "image_url", 
        "category", "source", "publication_date", "date","history_date").order_by("-history_id")


        return jsonify(list(history),status_code=200)


  #localhost:8000/history/?article=13
    elif(req.method == "POST"):
        article_id = req.GET.get("article", None)

        if article_id:
            article_id = int(article_id)
            history = list(ReadingHistory.objects.filter(user_id=user["user_id"], article_id=article_id))
            if history != []:
               history = ReadingHistory.objects.get(user_id=user["user_id"], article_id=article_id)
               history.history_date = datetime.now()
              
            else:
                history = ReadingHistory(user_id=user["user_id"], article_id=article_id)
            
            history.save()
    return jsonify({},status_code=200)



@csrf_exempt
@require_http_methods(["GET","POST", "DELETE"])
def bookmark(req):
    user = authenticate(req)

    if not user:
        return jsonify([])
        
    if(req.method == "GET"):
        bookmark = Bookmark.objects.filter(user_id=user["user_id"]).select_related('article').annotate(id=F('article__article_id')\
            ,title=F('article__title'),link=F('article__link'),summary=F('article__summary')\
                    ,description=F('article__description'),image_url=F('article__image_url'),\
                    category=F('article__category'),source=F('article__source'), publication_date=F('article__publication_date'), date=F('article__date')\
        ).values("id","title", "link", "summary", "description", "image_url", "category", "source", "publication_date", "date").order_by("-publication_date")
        
        
        return jsonify(list(bookmark),status_code=200)

    elif(req.method == "POST"):
        article_id = req.GET.get("article", None)

        if article_id:
            article_id = int(article_id)
            article = Article.objects.get(article_id = article_id)
            bookmark = Bookmark(user_id=user["user_id"], article=article)
            bookmark.save()

    #localhost:8000/bookmark/?article_id=1
    elif(req.method == "DELETE"):
        article_id = req.GET.get("article", None)
        if article_id:
            article_id = int(article_id)
            article = Article.objects.get(article_id = article_id)
            bookmark = Bookmark.objects.filter(article=article, user_id=user["user_id"])
            bookmark.delete()

    return jsonify([],status_code=200)


@csrf_exempt
@require_http_methods(["GET"])
def bookmark_article_ids(req):
    # localhost:8000/bookmark_article_ids
    user = authenticate(req)
    article_ids = list(Bookmark.objects.filter(user_id=user["user_id"]).select_related('article').\
        annotate(id=F('article__article_id')).values_list("id", flat=True))

    return jsonify({"data": article_ids},status_code=200)

@csrf_exempt
@require_http_methods(["GET","POST", "DELETE"])
def like_article(req):
    user = authenticate(req)

    if not user:
        return jsonify([])
        
    if(req.method == "GET"):
        likes = Likes.objects.filter(user_id=user["user_id"]).select_related('article').annotate(id=F('article__article_id')\
            ,title=F('article__title'),link=F('article__link'),summary=F('article__summary')\
                    ,description=F('article__description'),image_url=F('article__image_url'),\
                    category=F('article__category'),source=F('article__source'), publication_date=F('article__publication_date'), date=F('article__date')\
        ).values("id","title", "link", "summary", "description", "image_url", "category", "source", "publication_date", "date").order_by("-publication_date")
        
        
        return jsonify(list(likes),status_code=200)

    elif(req.method == "POST"):
        article_id = req.GET.get("article", None)

        if article_id:
            article_id = int(article_id)
            article = Article.objects.get(article_id = article_id)
            likes = Likes(user_id=user["user_id"], article=article)
            likes.save()

    #localhost:8000/like/?article_id=1
    elif(req.method == "DELETE"):
        article_id = req.GET.get("article", None)
        if article_id:
            article_id = int(article_id)
            article = Article.objects.get(article_id = article_id)
            likes = Likes.objects.filter(article=article, user_id=user["user_id"])
            likes.delete()

    return jsonify([],status_code=200)
    
@csrf_exempt
@require_http_methods(["GET"])
def like_article_ids(req):
    # localhost:8000/bookmark_article_ids
    user = authenticate(req)
    article_ids = list(Likes.objects.filter(user_id=user["user_id"]).select_related('article').\
        annotate(id=F('article__article_id')).values_list("id", flat=True))

    return jsonify({"data": article_ids},status_code=200)

@csrf_exempt
@require_http_methods(["POST"])
def not_interested(req):
	user = authenticate(req)
	article_id = req.GET.get("article", None)
	if article_id:
		 article_id = int(article_id)
		 article = Article.objects.get(article_id = article_id)	
		 not_interested = NotInterested(user_id=user["user_id"], article=article)
		 not_interested.save()
		 
	return jsonify([],status_code=200)
