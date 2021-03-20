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
from django.db.models import Max


@csrf_exempt
@require_http_methods(["GET"])
def search_suggestion(req):
    #localhost:8000/search_suggestion/?q=the
    search = req.GET.get("q", None)
    articles = Article.objects.order_by("-publication_date").filter(title__contains=search)[:5]
    articles = list(articles.values("article_id","title"))
    return jsonify(articles,status_code=200)


@csrf_exempt
@require_http_methods(["GET"])
def search_result(req):
    #localhost:8000/search_result/?article=15
    search = req.GET.get("q", "")

    if(search == ""):
        return jsonify([],status_code=200)

    articles = Article.objects.order_by("-publication_date").filter(title__contains=search)[:10]
    articles = list(articles.values())
    return jsonify(articles,status_code=200)


@csrf_exempt
@require_http_methods(["GET"])
def trend(req):
    # localhost:8000/trend
    trend_articles_id = ReadingHistory.objects.values("article_id").annotate(dcount=Count('article_id')).order_by('-dcount').values_list('article_id', flat=True)[:5]
    articles = Article.objects.filter(article_id__in=trend_articles_id)
    articles = list(articles.values())

    return jsonify(articles,status_code=200)