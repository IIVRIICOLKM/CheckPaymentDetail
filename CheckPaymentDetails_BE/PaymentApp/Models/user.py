from django.db import models
from datetime import datetime

class User(models.Model):
    id = models.AutoField(primary_key=True)
    password = models.IntegerField()
    name = models.CharField(max_length=10)
    registration_number = models.CharField(max_length=13)
    joined_at = models.DateTimeField(default=datetime.now())

    class Meta:
        db_table = 'user'