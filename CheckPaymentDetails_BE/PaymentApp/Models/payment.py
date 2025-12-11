from django.db import models

# https://docs.djangoproject.com/en/5.2/ref/models/fields/
# https://blog.naver.com/mym0404/221545140685

from .account import Account
from .place import Place
from .user import User

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    payment_day = models.DateTimeField()
    amount = models.IntegerField()
    balance = models.IntegerField()
    user_id = models.ForeignKey(
        User,
        db_column='user_id',
        on_delete=models.CASCADE,
        default=1,
    )
    account_id = models.ForeignKey(
        Account,
        db_column='account_id',
        on_delete=models.CASCADE,
    )
    # If Unique Key Type = CHAR, add to_field=
    account_number = models.ForeignKey(
        Account,
        db_column='account_number',
        to_field='number',
        on_delete=models.CASCADE,
    ),
    place_id = models.ForeignKey(
        Place,
        db_column='place_id',
        on_delete=models.CASCADE,
        default='',
        related_name='a'
    )

    class Meta:
        db_table = 'payment'