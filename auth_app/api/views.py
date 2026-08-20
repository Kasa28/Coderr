from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from profile_app.models import Profile
from .serializers import UserRegistrationSerializer

User = get_user_model()

class UserRegistrationView(APIView):
    """Register a user and return an authentication token."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            Profile.objects.create(user=user)
            token, _ = Token.objects.get_or_create(user=user)

            response_data = {
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.id,
            }

            return Response(
                response_data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class LoginView(APIView):
    """Authenticate a user and return an authentication token."""

    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request=request, username=username, password=password)

        if user is None:
            return Response(
                {"detail": "Benutzername oder Passwort ist falsch."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "username": user.username,
            "email": user.email,
            "user_id": user.id,
        })

