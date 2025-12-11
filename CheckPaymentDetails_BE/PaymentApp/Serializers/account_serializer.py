from rest_framework import serializers
from ..Models.account import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['account_id', 'account_number', 'bank_id']