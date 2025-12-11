from rest_framework import serializers
from ..Models.payment import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['payment_id', 'payment_day', 'account_id', 'account_number', 'payed_place', 'amount', 'balance']