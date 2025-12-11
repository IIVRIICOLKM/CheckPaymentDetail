from django.db import models
from .place_category import PlaceCategory

class Place(models.Model):
    place_name = models.CharField(primary_key=True, max_length=30)
    place_category_id = models.ForeignKey(PlaceCategory, on_delete=models.CASCADE, related_name='rnplacecategory', db_column='place_category_id', default=1)

    class Meta:
        db_table = 'place'