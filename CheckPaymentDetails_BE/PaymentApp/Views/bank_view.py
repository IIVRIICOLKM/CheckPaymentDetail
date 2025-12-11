from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from ..Models.bank import Bank
from ..Serializers.bank_serializer import BankSerializer
from rest_framework.permissions import AllowAny

class BankListView(APIView):
    permission_classes = [AllowAny]