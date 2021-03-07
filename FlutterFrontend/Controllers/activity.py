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
    # user = authenticate(req)
    # email = user["email"]
    email = "test3@test.com"
    user = retrieve_user(email)


    if(req.method == "GET"):
        itemsPerPage = 2

        page = req.GET.get("page", 1)
        page = int(page)
        offset = (page - 1) * itemsPerPage
        date = req.GET.get("dateRange", None)
       
        #for date filtering
        if not date:
            history = ReadingHistory.objects.filter(user=user)

        elif date:
            set_date_gt = datetime.now()
            set_date_lt = datetime.now()

            if date == "from 7 days ago":
                set_date_gt = datetime.now()-timedelta(days=7)
                set_date_lt = datetime.now() + timedelta(days=1)
       
            elif date == "from 14 days ago":
                set_date_lt = datetime.now()-timedelta(days=7)
                set_date_gt= datetime.now()-timedelta(days=14)


            history = ReadingHistory.objects.filter(user=user,history_date__gte=set_date_gt.strftime("%Y-%m-%d"), history_date__lt= set_date_lt.strftime("%Y-%m-%d"))
            

        history = history.select_related('article')\
                .annotate(id=F('article__article_id'),title=F('article__title'),link=F('article__link'),summary=F('article__summary')\
                ,description=F('article__description'),image_url=F('article__image_url'),\
                category=F('article__category'),source=F('article__source'), publication_date=F('article__publication_date'), date=F('article__date')\
        ).values("id","title", "link", 
        "summary", "description", "image_url", 
        "category", "source", "publication_date", "date","history_date").order_by("-publication_date")[offset:offset+itemsPerPage]
        return jsonify(list(history),status_code=200)


  #localhost:8000/history/?article=13
    elif(req.method == "POST"):
        article_id = req.GET.get("article", None)

        if article_id:
            article_id = int(article_id)
            article = Article.objects.get(article_id = article_id)
            read_history = ReadingHistory(user=user, article=article)
            try:
                read_history.save()
            except:
                print("history already saved")

    return jsonify({},status_code=200)



@csrf_exempt
@require_http_methods(["GET","POST", "DELETE"])
def bookmark(req):
    # user = authenticate(req)
    # email = user["email"]
    email = "test3@test.com"
    user = retrieve_user(email)

    if(req.method == "GET"):
        itemsPerPage = 2

        page = req.GET.get("page", 1)
        page = int(page)
        offset = (page - 1) * itemsPerPage 

        bookmark = Bookmark.objects.filter(user=user).select_related('article').annotate(id=F('article__article_id')\
            ,title=F('article__title'),link=F('article__link'),summary=F('article__summary')\
                    ,description=F('article__description'),image_url=F('article__image_url'),\
                    category=F('article__category'),source=F('article__source'), publication_date=F('article__publication_date'), date=F('article__date')\
        ).values("id","title", "link", "summary", "description", "image_url", "category", "source", "publication_date", "date").order_by("-publication_date")[offset:offset+itemsPerPage]
        
        
        return jsonify(list(bookmark),status_code=200)

    elif(req.method == "POST"):
        article_id = req.GET.get("article", None)

        if article_id:
            article_id = int(article_id)
            article = Article.objects.get(article_id = article_id)
            bookmark = Bookmark(user=user, article=article)
            bookmark.save()

    #localhost:8000/bookmark/?article_id=1
    elif(req.method == "DELETE"):
        article_id = req.GET.get("article", None)
        if article_id:
            article_id = int(article_id)
            article = Article.objects.get(article_id = article_id)
            bookmark = Bookmark.objects.filter(article=article, user=user)
            bookmark.delete()



    return jsonify({},status_code=200)
