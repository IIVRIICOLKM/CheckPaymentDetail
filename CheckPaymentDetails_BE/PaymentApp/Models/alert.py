from django.db import models
from datetime import datetime
from .user import User

class Alert(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(default=datetime.now())
    title = models.CharField(max_length=20)
    content = models.CharField(max_length=100)
    user_id = models.ForeignKey(
        User,
        to_field='id',
        db_column='user_id',
        on_delete=models.CASCADE
    )
    class Meta:
        db_table = 'alert'