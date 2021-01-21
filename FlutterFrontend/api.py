from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from database.models import User
from firebase_admin import auth
from .utils import *


initialize_firebase()

@csrf_exempt
@require_http_methods(["GET"])
def test1(req):
    user = auth.verify_id_token("")
    print(user)
    return HttpResponse(status=201)