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
                "Only business users can be reviewed."
            )

        return business_user


    def validate(self, data):
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