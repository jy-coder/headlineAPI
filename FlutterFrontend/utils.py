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

def retrieve_user(email):
	try:
		user = User.objects.get(email=email)
		return user
	except:
		return None

def authenticate(req):
	id_token = req.headers.get("X-Id-Token", None)

	if id_token:
		user = auth.verify_id_token(id_token)
	else:
		return None

	found_in_local = retrieve_user(user["email"])

	if found_in_local == None:
		return user
	else:
		return found_in_local
	


def error(message,status_code):
	return HttpResponse({"error": message},status=status_code,content_type="application/json")


def parse_json(req):
	return json.loads(req.body)


def jsonify(obj, status_code=None):
	return HttpResponse(json.dumps(obj, indent=4, sort_keys=True, default=str),status=status_code,content_type="application/json")



