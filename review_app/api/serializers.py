from rest_framework import serializers
from review_app.models import Review

class SerializerForReview(serializers.ModelSerializer):
    """Validate and create reviews for business users."""

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
        """Create a review using the authenticated user as its author."""
        logged_in_user = self.context["request"].user

        return Review.objects.create(
            reviewer=logged_in_user,
            **validated_data,
        )

    def validate_business_user(self, business_user):
        """Ensure that only business users can receive reviews."""
        if business_user.type != "business":
            raise serializers.ValidationError(
                "Only business users can be reviewed."
            )

        return business_user


    def validate(self, data):
        """Prevent a user from reviewing the same business user twice."""
        user = self.context["request"].user
        business_user = data.get(
            "business_user",
            self.instance.business_user if self.instance else None,
        )

        existing_review = Review.objects.filter(
            reviewer=user,
            business_user=business_user,
        )

        if self.instance:
            existing_review = existing_review.exclude(id=self.instance.id)

        if existing_review.exists():
            raise serializers.ValidationError(
                "You have already reviewed this business user."
            )

        return data


class WhenReviewUpdateSerializerAllowThisFields(serializers.ModelSerializer):
    """Allow only the rating and description of a review to change."""

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
            "business_user",
            "reviewer",
            "created_at",
            "updated_at",
        ]
