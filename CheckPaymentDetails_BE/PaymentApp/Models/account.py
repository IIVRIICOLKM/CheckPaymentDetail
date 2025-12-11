from django.db import models
from .bank import Bank
from .user import User
from datetime import datetime

class Account(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.CharField(unique=True, max_length=20, default='')
    created_at = models.DateTimeField(default=datetime.now())
    user_id = models.ForeignKey(
        User,
        db_column='user_id',
        to_field='id',
        on_delete=models.CASCADE,
        default=1,
    )
    bank_id = models.ForeignKey(
        Bank,
        db_column='bank_id',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.number

    class Meta:
        db_table = 'account'