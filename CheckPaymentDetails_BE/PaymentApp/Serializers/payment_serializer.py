from rest_framework import serializers
from ..Models.payment import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'payment_day', 'amount', 'balance', 'account_id', 'account_number', 'place_id', 'place_is_financial_transaction']