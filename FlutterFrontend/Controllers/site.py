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
def sites(req):
    #localhost:8000/sites
    sites = list(NewsSite.objects.values())
    return jsonify(sites,status_code=200)


@csrf_exempt
@require_http_methods(["GET"])
def site_subscription(req):
    #localhost:8000/site_subscription
    subscription = SiteSubscription.objects.filter(user_id=1)
    subscriptions = list(subscription.values())
    return jsonify(subscriptions,status_code=200)