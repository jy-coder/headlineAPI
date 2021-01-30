import firebase_admin 
from firebase_admin import auth, credentials
import os
from django.http import HttpResponse
import json
from django.forms.models import model_to_dict
from database.models import *


def initialize_firebase():
    FIREBASE_SERVICE = os.getenv("FIREBASE_SERVICE")
    cred = credentials.Certificate(FIREBASE_SERVICE)
    auth = firebase_admin.initialize_app(cred)


def authenticate(req):
	try:
		id_token = req.headers.get("X-Id-Token", "")
		# print(id_token)
		return auth.verify_id_token(id_token)
	except:
		return None

def error(message,status_code):
	return HttpResponse({"error": message},status=status_code,content_type="application/json")


def parse_json(req):
	return json.loads(req.body)



def jsonify(obj, status_code):
	return HttpResponse(json.dumps(obj, indent=4, sort_keys=True, default=str),status=status_code,content_type="application/json")

def retrieve_user(email):
	user = User.objects.get(email=email)
	return user


def save_subscription(records, user):



	for k,v in records.items():
		category = Category.objects.get(id =k)

		subscription = Subscription.objects.filter(user=user,category=category)
		# print(subscription)
	
		if v and not subscription:
			subscription = Subscription(user=user, category=category)
			subscription.save()

		elif not v and subscription:
			subscription = Subscription.objects.get(user=user,category=category)
			subscription.delete()


def get_subscription(user):
	records = []
	subscription = Subscription.objects.filter(user=user)
	category_id_list = list(subscription.values_list("category__id",flat=True))
	categories = list(Category.objects.values())
	# print(categories)
	for category in categories:
		category_id = category["id"]

		if(category_id in category_id_list):
			category["checked"] = True
		else:
			category["checked"] = False

		records.append(category)

	return records 
