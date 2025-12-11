from django.db import models
from PaymentApp.Models.bank import Bank
from datetime import datetime

class Account(models.Model):
    account_id = models.SmallIntegerField(primary_key=True)
    account_number = models.CharField(max_length=20, unique=True)
    bank_id = models.ForeignKey(Bank, on_delete=models.CASCADE, db_column='bank_id')
    account_registered_at = models.DateTimeField(default=datetime.now())
    account_updated_at = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.account_number

    class Meta:
        db_table = 'account'