from django.db import models

class PlaceCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=12)
    over_payed_flag = models.BooleanField(
        default=False
    )

    class Meta:
        db_table = 'place_category'