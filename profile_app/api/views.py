from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from profile_app.models import Profile
from profile_app.api.serializers import (ProfileSerializer, BusinessProfileSerializer, CustomerProfileSerializer,)
from profile_app.api.permissions import IsProfileOwnerOrReadOnly


class ProfileDetailView(generics.RetrieveUpdateAPIView):

    queryset = Profile.objects.select_related("user").all()
    serializer_class = ProfileSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        if self.request.method in ["PUT", "PATCH"]:
            return [IsProfileOwnerOrReadOnly()]
        return super().get_permissions()
    

    def get_object(self):
        user_id = self.kwargs.get("user_id")
        profile = get_object_or_404(
            Profile,
            user_id=user_id,
        )
        self.check_object_permissions(
            self.request,
            profile,
        )
        return profile


class BusinessProfileListView(generics.ListAPIView):
    serializer_class = BusinessProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.select_related("user").filter(
            user__type="business"
        )


class CustomerProfileListView(generics.ListAPIView):
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.select_related("user").filter(
            user__type="customer"
        )
