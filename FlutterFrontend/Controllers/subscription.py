from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from database.models import *
from firebase_admin import auth
from ..utils import *
from django.http import HttpResponse
from django.db.models import F
from datetime import datetime, timedelta
from django.forms.models import model_to_dict


def save_subscription(records, user):
	for k,v in records.items():
		category = Category.objects.get(category_id =k)

		subscription = Subscription.objects.filter(user=user,category=category)
        
		if v and not subscription:
			subscription = Subscription(user=user, category=category)
			subscription.save()

		elif not v and subscription:
			subscription = Subscription.objects.get(user=user,category=category)
			subscription.delete()


def get_subscription(user):
	records = []
	subscription = Subscription.objects.filter(user=user)
	category_id_list = list(subscription.values_list("category",flat=True))
	categories = list(Category.objects.values())

	for category in categories:
		category_id = category["category_id"]

		if(category_id in category_id_list):
			category["checked"] = True
		else:
			category["checked"] = False

		records.append(category)

	return records 


@csrf_exempt
@require_http_methods(["POST","GET"])
def subscription(req):
    user = authenticate(req)


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
def user_subscription(req):
    user = authenticate(req)
    if not user:
        return jsonify([], status_code=401)

    subscriptions = Subscription.objects.filter(user=user).select_related("category").values("category__category_name").annotate(category_name=F('category__category_name'))

    # include 'all' category
    all_dict = {}
    find_all = Category.objects.filter(category_name="all").first()
    all_dict["category_id"] = find_all.category_id
    all_dict["category_name"] = find_all.category_name
    

    subscriptions = list(subscriptions.values("category_name","category_id"))

    if(subscriptions != []):
        subscriptions.insert(0,all_dict)

    return jsonify(subscriptions,status_code=200)