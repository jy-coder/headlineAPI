import firebase_admin 
from firebase_admin import auth, credentials
import os

def initialize_firebase():
    FIREBASE_SERVICE = os.getenv("FIREBASE_SERVICE")
    cred = credentials.Certificate(FIREBASE_SERVICE)
    auth = firebase_admin.initialize_app(cred)


def authenticate(req):
	try:
		id_token = req.headers.get("x-id-token", "")
		return auth.verify_id_token(id_token)
	except:
		return None


def json(obj):
    return json.dumps(obj)