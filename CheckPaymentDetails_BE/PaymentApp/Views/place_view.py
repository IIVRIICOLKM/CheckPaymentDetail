from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

class PlaceView(APIView):
    permission_classes = [AllowAny]