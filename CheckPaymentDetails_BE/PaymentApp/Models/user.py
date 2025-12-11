from django.db import models
from datetime import datetime


class User(models.Model):
    id = models.CharField(primary_key=True, max_length=20)   # username 역할
    password = models.CharField(max_length=255)              # 해싱 저장 가능하도록 CharField로 변경
    name = models.CharField(max_length=10)
    registration_number = models.CharField(max_length=13, unique=True)
    joined_at = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = 'user'
