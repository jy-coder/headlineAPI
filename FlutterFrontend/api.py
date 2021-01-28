from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from database.models import *
from firebase_admin import auth
from .utils import *
from django.http import HttpResponse

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
    
   








