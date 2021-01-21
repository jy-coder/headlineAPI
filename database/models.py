
from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True, unique=True)
    email = models.CharField(default='', max_length=1000, blank=True)
    full_name = models.CharField(max_length=1000)

    class Meta:
        db_table = "User"