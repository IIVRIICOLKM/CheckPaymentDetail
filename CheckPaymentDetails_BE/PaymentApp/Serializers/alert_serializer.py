from rest_framework import serializers

from ..Models.alert import Alert

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['id', 'created_at', 'title', 'content', 'user_id']