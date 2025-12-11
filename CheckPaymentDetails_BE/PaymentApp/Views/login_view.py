from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from ..Models.user import User
from ..Serializers.user_serializer import SignupSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from ..Serializers.user_serializer import UserSerializer

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = SignupSerializer(data=request.data)

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save()

            return Response(
                {"message": "signup success", "user_id": user.id},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": "signup failed", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            user_id = request.data.get("id")
            password = request.data.get("password")

            # 입력값 검증
            if not user_id or not password:
                return Response(
                    {"error": "ID and password are required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 사용자 존재 여부 확인
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response(
                    {"error": "Invalid ID or password."},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # 비밀번호 검증
            if not check_password(password, user.password):
                return Response(
                    {"error": "Invalid ID or password."},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # JWT 발급
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "message": "login success",
                    "user": UserSerializer(user).data,
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh)
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": "login failed", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )