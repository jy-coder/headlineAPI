
import sys
sys.path.append("..")
import unittest
from  FlutterFrontend.utils import authenticate
from django.forms.models import model_to_dict
from database.models import User
from django.http import HttpResponse
from django.test import Client
csrf_client = Client(enforce_csrf_checks=True)
from firebase_admin import auth

class TestAuth(unittest.TestCase):
    # def test_register(self):
    #     c = Client()
    #     uid = 'G3B42XqrUuV0H0nexQqHzJCDz7A2'

    #     custom_token = auth.create_custom_token(uid).decode('ascii')
  
    #     c.post(
    #         '/register', 
    #    { "body": {"email": 'test@test.com'}, 
    #     "headers": {
    #       "Content-Type": "application/json",
    #       'Accept': 'application/json',
    #       "X-Id-Token": custom_token
    #     }})
            
        
    # def test_correct_email(self):
    #     email = "test@test.com"
    #     self.assertEqual("test@test.com", email)

    def test_wrong_email(self):
        c = Client()
        uid = 'FYCmXNPkj3aMTLPXdWFi3wAdPRo2'
        # custom_token = auth.create_custom_token(uid).decode('ascii')
        # user = auth.verify_id_token(custom_token)
        # auth.get_user(uid)

        # print(custom_token)

        # c.get("/recommend/?date=Three%20Days&category=&site=", 
        # { "headers": {
        #   "Content-Type": "application/json",
        #   'Accept': 'application/json',
        #   "X-Id-Token": custom_token
        # }})
  
        # print(custom_token)
# if __name__ == '__main__':
#     unittest.main()