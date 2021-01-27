import firebase_admin 
from firebase_admin import auth, credentials
import os
from django.http import HttpResponse
import json
from django.forms.models import model_to_dict

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


def jsonify(obj, status_code):
	return HttpResponse(json.dumps(obj),status=status_code,content_type="application/json")