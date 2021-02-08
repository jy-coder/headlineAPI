from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from database.models import *
from firebase_admin import auth
from .utils import *
from .Utils.subscription import *
from django.http import HttpResponse
from django.db.models import F

initialize_firebase()

@csrf_exempt
@require_http_methods(["GET"])
def test1(req):
    return HttpResponse(status=201)


@csrf_exempt
@require_http_methods(["GET"])
def category(req):
    # print(req.headers)
    user = authenticate(req)
    # print(user)
    # .order_by('-id')[:10][::-1]
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
        save_subscription(data, user)
        return jsonify({},status_code=200)

    elif(req.method == "GET"):
        subscriptions = get_subscription(user)
        return jsonify(subscriptions,status_code=200)

    return jsonify({},status_code=200)
    
   


@csrf_exempt
@require_http_methods(["GET"])
def article(req):
    itemsPerPage = 2

    page = req.GET.get("page", 1)
    category = req.GET.get("category", "all")

    print(category);


    page = int(page)
    offset = (page - 1) * itemsPerPage + 1
    # user = authenticate(req)
    # email = user["email"]
    # user = retrieve_user(email)

     #localhost:8000/article/?page=1
    if category == "all":
        articles = Article.objects.order_by("-publication_date")[offset:offset+itemsPerPage].annotate(id=F('article_id'))
   
    #localhost:8000/article/?page=2&category=business
    #localhost:8000/article/?page=3&category=all
    else:
        articles = Article.objects.filter(category=category).order_by("-publication_date")[offset:offset+itemsPerPage].annotate(id=F('article_id'))


    articles = list(articles.values())
    # print(articles)

    return jsonify(articles,status_code=200)
    

@csrf_exempt
@require_http_methods(["GET"])
def history(req):
    if(req.method == "GET"):
        itemsPerPage = 2

        page = req.GET.get("page", 1)
        page = int(page)
        offset = (page - 1) * itemsPerPage + 1
        # user = authenticate(req)
        # email = user["email"]
        email = "bee@test.com"
        user = retrieve_user(email)
        history = ReadingHistory.objects.filter(user=user).select_related('article')\
                .annotate(id=F('article__article_id'),title=F('article__title'),link=F('article__link'),summary=F('article__summary')\
                ,description=F('article__description'),image_url=F('article__image_url'),\
                category=F('article__category'),source=F('article__source'), publication_date=F('article__publication_date'), date=F('article__date')\
        ).values("id","title", "link", 
        "summary", "description", "image_url", 
        "category", "source", "publication_date", "date").order_by("-publication_date")[offset:offset+itemsPerPage]
        return jsonify(list(history),status_code=200)


    elif(req.method == "POST"):
        user = authenticate(req)
        email = user["email"]
        # email = "bee@test.com"
        user = retrieve_user(email)

        #localhost:8000/history/?article=13
        article_id = req.GET.get("article", None)

        if article_id:
            article_id = int(article_id)
            article = Article.objects.get(article_id = article_id)
            read_history = ReadingHistory(user=user, article=article)
            read_history.save()

    

    return jsonify({},status_code=200)
    
    
 


@csrf_exempt
@require_http_methods(["POST"])
def save_history(req):
    user = authenticate(req)
    email = user["email"]
    # email = "bee@test.com"
    user = retrieve_user(email)

    #localhost:8000/history/?article=13
    article_id = req.GET.get("article", None)

    if article_id:
        article_id = int(article_id)
        article = Article.objects.get(article_id = article_id)
        read_history = ReadingHistory(user=user, article=article)
        read_history.save()

    

    return jsonify({},status_code=200)
    


