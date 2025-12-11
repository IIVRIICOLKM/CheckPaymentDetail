from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

class PlaceCategoryView(APIView):
    permission_classes = [AllowAny]