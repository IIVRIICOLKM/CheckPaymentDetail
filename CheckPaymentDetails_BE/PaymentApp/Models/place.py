from django.db import models
from .place_category import PlaceCategory

# class Place(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(
#         unique=True,
#         max_length=30,
#         default=''
#     )
#     place_category_id = models.ForeignKey(
#         PlaceCategory,
#         on_delete=models.CASCADE,
#         db_column='id',
#         default=1
#     ),
#     is_financial_transaction = models.BooleanField(
#         default=False
#     )
#
#     class Meta:
#         db_table = 'place'

class Place(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(
        unique=True,
        max_length=30,
        default=''
    )

    # 콤마 제거 + db_column 정상화
    place_category_id = models.ForeignKey(
        PlaceCategory,
        on_delete=models.CASCADE,
        db_column='place_category_id',
        default=1
    )

    is_financial_transaction = models.BooleanField(default=False)

    class Meta:
        db_table = 'place'
