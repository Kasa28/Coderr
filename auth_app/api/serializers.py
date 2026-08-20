from rest_framework import serializers
from auth_app.models import CoderrUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Validate registration data and create a new user account."""

    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = CoderrUser
        fields = [
            "username",
            "email",
            "password",
            "repeated_password",
            "type",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, data):
        """Ensure that both submitted passwords match."""
        if data["password"] != data["repeated_password"]:
            raise serializers.ValidationError({
                 "Die Passwörter stimmen nicht überein."
            })

        return data

    def create(self, validated_data):
        """Create a user while hashing the submitted password."""
        validated_data.pop("repeated_password")

        user = CoderrUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            type=validated_data["type"],
        )

        return user
