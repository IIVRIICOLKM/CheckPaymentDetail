from rest_framework import serializers

from ..Models.place import PlaceCategory

class PlaceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceCategory
        fields = ['id', 'name', 'place_category_id']