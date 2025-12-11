from rest_framework import serializers

from ..Models.user import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'password', 'name', 'registration_number', 'joined_at']