from django.urls import path
from review_app.api.views import ReviewDetailView, ReviewsView

urlpatterns = [
    path("reviews/", ReviewsView.as_view(), name="review-list-create"),
    path("reviews/<int:pk>/", ReviewDetailView.as_view(), name="review-detail")
]
