from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from database.models import *
from firebase_admin import auth
from .utils import *
from django.http import HttpResponse
from django.db.models import F
from datetime import datetime, timedelta
from django.forms.models import model_to_dict

initialize_firebase()

@csrf_exempt
@require_http_methods(["GET"])
def test1(req):        
    return jsonify({}, status_code=200)




   