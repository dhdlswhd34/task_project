from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

from django.contrib.auth import authenticate

from task.models.users import User


# 회원가입
class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        if not email or not password:
            return Response(
                {"message": "Email and password required"}, status=400
            )
        if User.objects.filter(email=email).exists():
            return Response({"message": "User already exists"}, status=400)
        user = User.objects.create_user(email=email, password=password)
        return Response({"email": user.email}, status=201)


# 로그인
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)
        if user is None:
            return Response({"message": "Invalid credentials"}, status=400)
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
        )
