from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from ..Models.user import User

class KakaoLoginView(APIView):
    permission_classes = [AllowAny]