from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from ..Models.account import Account
from ..Serializers.account_serializer import AccountSerializer
from rest_framework.permissions import AllowAny

class AccountListView(APIView):
    permission_classes = [AllowAny]