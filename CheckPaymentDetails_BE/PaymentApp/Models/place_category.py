from django.db import models

class PlaceCategory(models.Model):
    place_category_id = models.AutoField(primary_key=True)
    place_category_name = models.CharField(max_length=12)

    class Meta:
        db_table = 'place_category'