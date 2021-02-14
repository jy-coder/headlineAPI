from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from database.models import *
from firebase_admin import auth
from .utils import *
from .Utils.subscription import *
from django.http import HttpResponse
from django.db.models import F
from datetime import datetime, timedelta

initialize_firebase()

@csrf_exempt
@require_http_methods(["GET"])
def test1(req):
    return HttpResponse(status=201)


@csrf_exempt
@require_http_methods(["GET"])
def category(req):
    user = authenticate(req)
    categories = list(Category.objects.values())
    return jsonify(categories, status_code=200)


@csrf_exempt
@require_http_methods(["POST"])
def register(req):
    user = authenticate(req)
    save_user = User(uuid=user[
        "user_id"], email=user["email"])
    save_user.save()
    return HttpResponse(status=201)


@csrf_exempt
@require_http_methods(["POST","GET"])
def subscription(req):
    user = authenticate(req)
    email = user["email"]
    user = retrieve_user(email)

    if(req.method == "POST"):
        data = parse_json(req)
        print(data);
        save_subscription(data, user)
        return jsonify({},status_code=200)

    elif(req.method == "GET"):
        subscriptions = get_subscription(user)
        return jsonify(subscriptions,status_code=200)

    return jsonify({},status_code=200)

@csrf_exempt
@require_http_methods(["GET"])
def user_subscription(req):
    # user = authenticate(req)
    # email = user["email"]
    email = "test3@test.com"
    user = retrieve_user(email)
    subscriptions = Subscription.objects.filter(user=user).select_related("category").values("category__category_name").annotate(category_name=F('category__category_name'))

   
    # include 'all' category
    all_dict = {}
    find_all = Category.objects.filter(category_name="all").first()
    all_dict["category_id"] = find_all.category_id
    all_dict["category_name"] = find_all.category_name
    

    subscriptions = list(subscriptions.values("category_name","category_id"))

    if(len(subscriptions) != 0):
        subscriptions.insert(0,all_dict)

    return jsonify(subscriptions,status_code=200)

    

@csrf_exempt
@require_http_methods(["GET"])
def article(req):
    # user = authenticate(req)
    # email = user["email"]
    email = "test3@test.com"
  
    user = retrieve_user(email)

    itemsPerPage = 2

    page = req.GET.get("page", 1)
    category = req.GET.get("category", "all")

    page = int(page)
    start = (page - 1) * itemsPerPage
    end = page * itemsPerPage

    #localhost:8000/article/?page=1
    #localhost:8000/article/?page=2&category=business
    #localhost:8000/article/?page=3&category=all
    if category != "all":
        articles = Article.objects.filter(category=category)
    else:
       articles = Article.objects.all() 
     


    if user:
        bookmarks_id_list = list(Bookmark.objects.filter(user=user).values_list("article__article_id",flat=True))
        articles = articles.exclude(article_id__in=bookmarks_id_list)
      

    articles = articles.order_by("-publication_date")[start:end].annotate(id=F('article_id'))
  
    articles = list(articles.values())
  
    # print(articles)

    return jsonify(articles,status_code=200)
    

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
        offset = (page - 1) * itemsPerPage + 1
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


            history = ReadingHistory.objects.filter(user=user,history_date__gte=set_date_gt.strftime("%Y-%m-%d"), history_date__lt= set_date_lt)
            

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
            read_history.save()

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
        offset = (page - 1) * itemsPerPage + 1

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


#localhost:8000/search_suggestion/?q=the
@csrf_exempt
@require_http_methods(["GET"])
def search_suggestion(req):
    search = req.GET.get("q", None)
    articles = Article.objects.order_by("-publication_date").filter(title__contains=search)[:5]
    articles = list(articles.values("article_id","title"))
    return jsonify(articles,status_code=200)


#localhost:8000/search_result/?article=15
@csrf_exempt
@require_http_methods(["GET"])
def search_result(req):
    search = req.GET.get("q", "")

    if(search == ""):
        return jsonify([],status_code=200)

    articles = Article.objects.order_by("-publication_date").filter(title__contains=search)[:10]
    articles = list(articles.values())
    # article_id = req.GET.get("article", None)
    # articles = Article.objects.filter(article_id=article_id)
    # articles = list(articles.values())
    return jsonify(articles,status_code=200)
   