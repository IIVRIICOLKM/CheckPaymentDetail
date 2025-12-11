from rest_framework import serializers

from ..Models.place import Place

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['id', 'name', 'place_category_id']