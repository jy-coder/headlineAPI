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
       
        # for date filtering
        # if not date:
        #     history = ReadingHistory.objects.filter(user_id=user["user_id"])

        # elif date:
        #     set_date_gt = datetime.now()
        #     set_date_lt = datetime.now()

        #     if date == "from 7 days ago":
        #         set_date_gt = datetime.now()-timedelta(days=7)
        #         set_date_lt = datetime.now() + timedelta(days=1)
       
        #     elif date == "from 14 days ago":
        #         set_date_lt = datetime.now()-timedelta(days=7)
        #         set_date_gt= datetime.now()-timedelta(days=14)


            # history = ReadingHistory.objects.filter(user_id=user["user_id"],history_date__gte=set_date_gt.strftime("%Y-%m-%d"))

    
        # print(history)
 

        history = ReadingHistory.objects.filter(user_id=user["user_id"]).select_related('article')\
                .annotate(id=F('article__article_id'),title=F('article__title'),link=F('article__link'),summary=F('article__summary')\
                ,description=F('article__description'),image_url=F('article__image_url'),\
                category=F('article__category'),source=F('article__source'), publication_date=F('article__publication_date'), date=F('article__date')\
        ).values("id","title", "link", 
        "summary", "description", "image_url", 
        "category", "source", "publication_date", "date","history_date").order_by("-publication_date")


        return jsonify(list(history),status_code=200)


  #localhost:8000/history/?article=13
    elif(req.method == "POST"):
        article_id = req.GET.get("article", None)

        if article_id:
            article_id = int(article_id)
            article = Article.objects.get(article_id = article_id)
            read_history = ReadingHistory(user_id=user["user_id"], article=article)
            try:
                read_history.save()
            except:
                print("history already saved")

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
