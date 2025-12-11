from django.db import models

class Bank(models.Model):
    bank_id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    phone_num = models.CharField(max_length=8)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'bank'