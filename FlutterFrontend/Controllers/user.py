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
@require_http_methods(["POST"])
def register(req):
    user = authenticate(req)
    save_user = User(uuid=user["uid"],email=user["email"])
    try:
        save_user.save()
    except:
        return HttpResponse(status=403)
        
    return HttpResponse(status=201)




