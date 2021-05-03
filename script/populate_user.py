import os
import sys
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import django
django.setup()
from database.models import *




if __name__ == '__main__':
    user = User(email="test@test.com")
    user.save()
    print("user saved to databse")


