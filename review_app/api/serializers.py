from rest_framework import serializers
from review_app.models import Review

class SerializerForReview(serializers.ModelSerializer):
    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "reviewer",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        logged_in_user = self.context["request"].user

        return Review.objects.create(
            reviewer=logged_in_user,
            **validated_data,
        )

    def validate_business_user(self, business_user):
        if business_user.type != "business":
            raise serializers.ValidationError(
                "Nur Business-User können bewertet werden!."
            )

        return business_user