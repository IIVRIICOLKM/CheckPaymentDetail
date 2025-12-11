from rest_framework import serializers
from ..Models.bank import Bank

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ['id', 'name', 'phone_num']