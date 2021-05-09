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

# deprecated
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
    #localhost:8000/search_result/?q=fan
    search = req.GET.get("q", "")

    if(search == ""):
        return jsonify([],status_code=200)

    articles = Article.objects.order_by("-publication_date").annotate(id=F('article_id')).filter(title__icontains=search)[:10]
    articles = list(articles.values())
    return jsonify(articles,status_code=200)