from django.db import models

class Bank(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    phone_num = models.CharField(max_length=8)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'bank'