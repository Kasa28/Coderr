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


class GuestLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_type = request.data.get("type")

        if user_type not in ["customer", "business"]:
            return Response(
                {"detail": "Type should be customer or business."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        username = f"guest_{user_type}"
        guest_user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "type": user_type, "email": f"{username}@example.com",
            },
        )

        if created:
            guest_user.set_unusable_password()
            guest_user.save(update_fields=["password"])

        Profile.objects.get_or_create(user=guest_user)
        token, _ = Token.objects.get_or_create(user=guest_user)

        return Response({
            "token": token.key,
            "username": guest_user.username,
            "email": guest_user.email,
            "user_id": guest_user.id,
        })
